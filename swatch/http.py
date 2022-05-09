"""Main http service that handles starting app modules."""

from flask import (
    Blueprint,
    Flask,
    current_app,
    jsonify,
    make_response,
    request,
)

from swatch.image import ImageProcessor

bp = Blueprint("swatch", __name__)

def create_app(
    swatch_config,
    image_processor: ImageProcessor,
):
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config = swatch_config
    app.image_processor = image_processor
    return app

### Basic / Frontend Routes


@bp.route("/")
def status():
    """Return Swatch stats."""
    return "Swatch is running."


### API Routes


@bp.route("/api/config", methods=["GET"])
def get_config():
    """Get current config."""
    return make_response(jsonify(current_app.config.dict()), 200)


@bp.route("/api/<camera_name>/detect", methods=["POST"])
def detect_camera_frame(camera_name):
    """Use camera frame to detect known objects."""
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    camera_config = current_app.config.cameras.get(camera_name)

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
        result = current_app.image_processor.detect(camera_name, image_url)

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
def get_latest_result(label):
    """Get the latest results for a label"""
    if not label:
        return make_response(
            jsonify({"success": False, "message": "Label needs to be provided"})
        )

    return current_app.image_processor.get_latest_result(label)


@bp.route("/api/colortest", methods=["POST"])
def test_colors():
    """Test and get color values inside of test image."""
    if not request.files or not request.files.get("test_image"):
        return make_response(
            jsonify(
                {"success": False, "message": "An image needs to be sent as test_image"}
            )
        )

    test_image = request.files.get("test_image")
    main_color, palette = current_app.image_processor.parse_colors_from_image(test_image)

    return make_response(
        jsonify(
            {
                "success": True,
                "message": f"The dominant color is {main_color} with a mixed palette as {palette}",
            }
        )
    )
