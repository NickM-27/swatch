import base64
from swatch import SwatchService
from flask import (
    Blueprint,
    Flask,
    Response,
    current_app,
    jsonify,
    make_response,
    request,
)

app = Flask(__name__)
swatch = SwatchService()

@app.route('/')
def status():
    return "Swatch is running."

@app.route('/api/<camera_name>/detect', methods=['POST'])
def detect_camera_frame(camera_name):
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    if not swatch.config.cameras[camera_name]:
        return make_response(
            jsonify({"success": False, "message": f"{camera_name} is not a camera in the config."}), 404
        )
    
    if request.json:
        image_url = request.json.get("imageUrl")
        result = swatch.detect(camera_name, image_url)

        if result:
            return make_response(
                jsonify(result), 200
            )
        else:
            return make_response(
                jsonify({"success": False, "message": "Unknown error doing detection."}), 500
            )
    else:
        return make_response(
            jsonify({"success": False, "message": "image url must be set."}), 404
        )