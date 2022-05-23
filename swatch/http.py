"""Main http service that handles starting app modules."""

from functools import reduce
import logging
from typing import Any, Dict

from flask import (
    Blueprint,
    Flask,
    current_app,
    jsonify,
    make_response,
    request,
)

from peewee import DoesNotExist, operator
from playhouse.shortcuts import model_to_dict

from swatch.config import CameraConfig, SwatchConfig, ZoneConfig
from swatch.image import ImageProcessor
from swatch.models import Detection
from swatch.snapshot import SnapshotProcessor

bp = Blueprint("swatch", __name__)


def create_app(
    swatch_config: SwatchConfig,
    image_processor: ImageProcessor,
    snapshot_processor: SnapshotProcessor,
) -> Flask:
    """Creates the Flask app to run the webserver."""
    app = Flask(__name__)
    disable_logs()
    app.register_blueprint(bp)
    app.swatch_config = swatch_config
    app.image_processor = image_processor
    app.snapshot_processor = snapshot_processor
    return app


### Basic / Frontend Routes


@bp.route("/")
def status() -> str:
    """Return Swatch stats."""
    return "Swatch is running."


### Config API Routes


@bp.route("/config", methods=["GET"])
def get_config() -> Any:
    """Get current config."""
    return make_response(jsonify(current_app.swatch_config.dict()), 200)


@bp.route("/colortest/values", methods=["POST"])
def test_colors() -> Any:
    """Test and get color values inside of test image."""
    if not request.files or not request.files.get("test_image"):
        return make_response(
            jsonify(
                {"success": False, "message": "An image needs to be sent as test_image"}
            ),
            404,
        )

    test_image = request.files.get("test_image")
    main_color, palette = current_app.image_processor.parse_colors_from_image(
        test_image
    )

    return make_response(
        jsonify(
            {
                "success": True,
                "message": f"The dominant color is {main_color} with a mixed palette as {palette}",
            }
        ),
        404,
    )


@bp.route("/colortest/mask", methods=["POST"])
def test_mask() -> Any:
    """Test and get masked image for given lower and upper color values."""
    if not request.files or not request.files.get("test_image"):
        return make_response(
            jsonify(
                {"success": False, "message": "An image needs to be sent as test_image"}
            ),
            404,
        )

    if not request.form.get("color_lower") or not request.form.get("color_upper"):
        return make_response(
            jsonify(
                {
                    "success": False,
                    "message": "color_lower and color_upper need to be provided",
                }
            ),
            404,
        )

    image_str = request.files.get("test_image").read()
    color_lower = request.form.get("color_lower")
    color_upper = request.form.get("color_upper")

    masked_image = current_app.image_processor.mask_test_image(
        image_str, color_lower, color_upper
    )

    if not masked_image:
        return make_response(
            jsonify(
                {
                    "success": False,
                    "message": "color_lower and color_upper need to be provided",
                }
            ),
            500,
        )

    response = make_response(masked_image)
    response.headers["Content-Type"] = "image/jpg"
    return response


### Detection API Routes


@bp.route("/detections", methods=["GET"])
def get_detections() -> Any:
    """Get detections from the db."""
    limit = request.args.get("limit", 100)
    camera = request.args.get("camera", "all")
    label = request.args.get("label", "all")
    zone = request.args.get("zone", "all")
    after = request.args.get("after", type=float)
    before = request.args.get("before", type=float)

    clauses = []
    excluded_fields = []

    selected_columns = [
        Detection.id,
        Detection.camera,
        Detection.label,
        Detection.zone,
        Detection.top_area,
        Detection.color_variant,
        Detection.start_time,
    ]

    if camera != "all":
        clauses.append(Detection.camera == camera)

    if label != "all":
        clauses.append(Detection.label == label)

    if zone != "all":
        clauses.append(Detection.zone.cast("text") % f'*"{zone}"*')

    if after:
        clauses.append(Detection.start_time > after)

    if before:
        clauses.append(Detection.start_time < before)

    if len(clauses) == 0:
        clauses.append(True)

    detections = (
        Detection.select(*selected_columns)
        .where(reduce(operator.and_, clauses))
        .order_by(Detection.start_time.desc())
        .limit(limit)
    )

    return jsonify([model_to_dict(d, exclude=excluded_fields) for d in detections])


@bp.route("/detections/<detection_id>", methods=["GET"])
def get_detection(id: str):
    """Get specific detection."""
    try:
        return model_to_dict(Detection.get(Detection.id == id))
    except DoesNotExist:
        return jsonify(
            {"success": False, "message": f"Detection with id {id} not found."}, 404
        )


@bp.route("/<camera_name>/detect", methods=["POST"])
def detect_camera_frame(camera_name: str) -> Any:
    """Use camera frame to detect known objects."""
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    camera_config: CameraConfig = current_app.swatch_config.cameras.get(camera_name)

    if not camera_config:
        return make_response(
            jsonify(
                {
                    "success": False,
                    "message": f"{camera_name} is not a camera in the config.",
                }
            ),
            404,
        )

    if (
        not (request.json and request.json.get("imageUrl"))
        and camera_config.snapshot_config.url
    ):
        image_url = camera_config.snapshot_config.url
    elif request.json:
        image_url = request.json.get("imageUrl")
    else:
        image_url = None

    if image_url:
        try:
            result: Dict[str, Any] = current_app.image_processor.detect(
                camera_name, image_url
            )
        except Exception as _e:
            return make_response(
                jsonify(
                    {
                        "success": False,
                        "message": f"{image_url} is invalid or does not contain a valid image: {_e}.",
                    }
                ),
                404,
            )

        if result:
            return make_response(jsonify(result), 200)

        return make_response(
            jsonify({"success": False, "message": "Unknown error doing detection."}),
            500,
        )

    return make_response(
        jsonify(
            {
                "success": False,
                "message": "image url must be passed or set in the config.",
            }
        ),
        404,
    )


@bp.route("/<label>/latest", methods=["GET"])
def get_latest_result(label: str) -> Any:
    """Get the latest results for a label"""
    if not label:
        return make_response(
            jsonify({"success": False, "message": "Label needs to be provided"})
        )

    return current_app.image_processor.get_latest_result(label)

    ### Snapshot API Routes


@bp.route("/<camera_name>/snapshot.jpg", methods=["GET"])
def get_latest_camera_snapshot(camera_name: str) -> Any:
    """Get the latest snapshot for <camera_name>."""
    if not camera_name:
        return jsonify(
            {"success": False, "message": "camera_name must be provided."}, 404
        )

    camera_config = current_app.swatch_config.cameras.get(camera_name)

    if not camera_config:
        return jsonify(
            {"success": False, "message": f"{camera_name} is not a valid camera."}, 404
        )

    jpg_bytes = current_app.snapshot_processor.get_latest_camera_snapshot(camera_name)

    if not jpg_bytes:
        return jsonify(
            {"success": False, "message": "Failed to load image from camera."}, 500
        )

    response = make_response(jpg_bytes)
    response.headers["Content-Type"] = "image/jpg"
    return response


@bp.route("/<camera_name>/<zone_name>/snapshot.jpg", methods=["GET"])
def get_latest_zone_snapshot(camera_name: str, zone_name: str) -> Any:
    """Get the latest snapshot for <camera_name>."""
    if not camera_name:
        return jsonify(
            {"success": False, "message": "camera_name must be provided."}, 404
        )

    camera_config: CameraConfig() = current_app.swatch_config.cameras.get(camera_name)

    if not camera_config:
        return jsonify(
            {"success": False, "message": f"{camera_name} is not a valid camera."}, 404
        )

    if not zone_name:
        return jsonify(
            {"success": False, "message": "zone_name must be provided."}, 404
        )

    zone_config: ZoneConfig = camera_config.zones.get(zone_name)

    if not zone_config:
        return jsonify(
            {
                "success": False,
                "message": f"{zone_name} is not a valid zone for {camera_name}.",
            },
            404,
        )

    jpg_bytes = current_app.snapshot_processor.get_latest_zone_snapshot(
        camera_name, zone_name
    )

    if not jpg_bytes:
        return jsonify(
            {"success": False, "message": "Failed to load image from camera."}, 500
        )

    response = make_response(jpg_bytes)
    response.headers["Content-Type"] = "image/jpg"
    return response


@bp.route("/<camera_name>/detection.jpg", methods=["GET"])
def get_latest_detection(camera_name: str) -> Any:
    """Get the latest detection for <camera_name>."""
    if not camera_name:
        return jsonify(
            {"success": False, "message": "camera_name must be provided."}, 404
        )

    camera_config = current_app.swatch_config.cameras.get(camera_name)

    if not camera_config:
        return jsonify(
            {"success": False, "message": f"{camera_name} is not a valid camera."}, 404
        )

    jpg_bytes = current_app.snapshot_processor.get_latest_detection(camera_name)

    response = make_response(jpg_bytes)
    response.headers["Content-Type"] = "image/jpg"
    return response


### Util Funs


def disable_logs():
    """Disable flask logs"""
    flask_logger = logging.getLogger("werkzeug")
    flask_logger.disabled = True
