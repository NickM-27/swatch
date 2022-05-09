from swatch import SwatchService

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)

from waitress import serve

app = Flask(__name__)
swatch = SwatchService()

### Basic / Frontend Routes


@app.route("/")
def status():
    """Return Swatch stats."""
    return "Swatch is running."


### API Routes


@app.route("/api/config", methods=["GET"])
def get_config():
    """Get current config."""
    return make_response(jsonify(swatch.config.dict()), 200)


@app.route("/api/<camera_name>/detect", methods=["POST"])
def detect_camera_frame(camera_name):
    """Use camera frame to detect known objects."""
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    camera_config = swatch.config.cameras.get(camera_name)

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
        result = swatch.image_processor.detect(camera_name, image_url)

        if result:
            return make_response(jsonify(result), 200)

        return make_response(
            jsonify(
                {"success": False, "message": "Unknown error doing detection."}
            ),
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


@app.route("/api/<label>/latest", methods=["GET"])
def get_latest_result(label):
    """Get the latest results for a label"""
    if not label:
        return make_response(
            jsonify(
                {"success": False, "message": "Label needs to be provided"}
            )
        )

    return swatch.image_processor.get_latest_result(label)


@app.route("/api/colortest", methods=["POST"])
def test_colors():
    """Test and get color values inside of test image."""
    if not request.files or not request.files.get("test_image"):
        return make_response(
            jsonify(
                {"success": False, "message": "An image needs to be sent as test_image"}
            )
        )

    test_image = request.files.get("test_image")
    main_color, palette = swatch.image_processor.parse_colors_from_image(test_image)

    return make_response(
        jsonify(
            {
                "success": True,
                "message": f"The dominant color is {main_color} with a mixed palette as {palette}",
            }
        )
    )


if __name__ == "__main__":
    serve(app, listen="*:4500")
