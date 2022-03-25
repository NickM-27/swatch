import base64
import json

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

from waitress import serve

app = Flask(__name__)
swatch = SwatchService()

### Basic / Frontend Routes

@app.route('/')
def status():
    return "Swatch is running."

### API Routes

@app.route('/api/config', methods=['GET'])
def get_config():
    return make_response(jsonify(swatch.config.dict()), 200)

@app.route('/api/<camera_name>/detect', methods=['POST'])
def detect_camera_frame(camera_name):
    if not camera_name:
        return make_response(
            jsonify({"success": False, "message": "camera_name must be set."}), 404
        )

    if not swatch.config.cameras.get(camera_name):
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

if __name__ == "__main__":
    serve(app, listen='*:4500')