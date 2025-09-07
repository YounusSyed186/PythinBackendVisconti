from flask import Blueprint, request, jsonify
from controllers.menuuploadControllers import (
    get_menu_images,
    upload_menu_image,
    delete_menu_image
)
from multer import save_uploaded_file  # multer equivalent

image_bp = Blueprint("image", __name__)

# ---------------- IMAGE ROUTES ----------------

# GET all images
@image_bp.route("/images", methods=["GET"])
def get_images():
    return get_menu_images()

# POST upload new image
@image_bp.route("/images", methods=["POST"])
def add_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400
    file_path = save_uploaded_file(file)
    return upload_menu_image(file_path)

# DELETE image by ID
@image_bp.route("/images/<id>", methods=["DELETE"])
def remove_image(id):
    return delete_menu_image(id)
