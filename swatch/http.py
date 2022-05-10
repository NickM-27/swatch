"""Main http service that handles starting app modules."""

from typing import Any, Dict
from flask import (
    Blueprint,
    Flask,
    current_app,
    jsonify,
    make_response,
    request,
)

from swatch.config import CameraConfig, SwatchConfig
from swatch.image import ImageProcessor

bp = Blueprint("swatch", __name__)


def create_app(
    swatch_config: SwatchConfig,
    image_processor: ImageProcessor,
) -> Flask:
    """Creates the Flask app to run the webserver."""
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.swatch_config = swatch_config
    app.image_processor = image_processor  # type: ignore[attr-defined]
    return app


### Basic / Frontend Routes


@bp.route("/")
def status() -> str:
    """Return Swatch stats."""
    return "Swatch is running."


### API Routes


@bp.route("/api/config", methods=["GET"])
def get_config() -> Any:
    """Get current config."""
    return make_response(jsonify(current_app.swatch_config.dict()), 200)  # type: ignore[attr-defined]


@bp.route("/api/<camera_name>/detect", methods=["POST"])
def detect_camera_frame(camera_name: str) -> Any:
    """Use camera frame to detect known objects."""
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    camera_config: CameraConfig = current_app.swatch_config.cameras.get(camera_name)  # type: ignore[attr-defined]

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
        and camera_config.snapshot_url
    ):
        image_url = camera_config.snapshot_url
    elif request.json:
        image_url = request.json.get("imageUrl")
    else:
        image_url = None

    if image_url:
        result: Dict[str, Any] = current_app.image_processor.detect(camera_name, image_url)  # type: ignore[attr-defined]

        if result:
            return make_response(jsonify(result), 200)

        return make_response(
            jsonify({"success": False, "message": "Unknown error doing detection."}),
            500,
        )
    else:
        return make_response(
            jsonify(
                {
                    "success": False,
                    "message": "image url must be passed or set in the config.",
                }
            ),
            404,
        )


@bp.route("/api/<label>/latest", methods=["GET"])
def get_latest_result(label: str) -> Any:
    """Get the latest results for a label"""
    if not label:
        return make_response(
            jsonify({"success": False, "message": "Label needs to be provided"})
        )

    return current_app.image_processor.get_latest_result(label)  # type: ignore[attr-defined]


@bp.route("/api/colortest", methods=["POST"])
def test_colors() -> Any:
    """Test and get color values inside of test image."""
    if not request.files or not request.files.get("test_image"):
        return make_response(
            jsonify(
                {"success": False, "message": "An image needs to be sent as test_image"}
            )
        )

    test_image = request.files.get("test_image")
    main_color, palette = current_app.image_processor.parse_colors_from_image(test_image)  # type: ignore[attr-defined]

    return make_response(
        jsonify(
            {
                "success": True,
                "message": f"The dominant color is {main_color} with a mixed palette as {palette}",
            }
        )
    )
