from flask import Blueprint, request, jsonify
from controllers.menuControllers import (
    get_all_menu_items,
    add_menu_item,
    edit_menu_item,
    delete_menu_item
)
from multer import save_uploaded_file  # our multer-equivalent

menu_bp = Blueprint("menu", __name__)

# ---------------- MENU ROUTES ----------------

# GET all menu items
@menu_bp.route("/", methods=["GET"])
def get_menu_items():
    return get_all_menu_items()

# POST new menu item with image
@menu_bp.route("/", methods=["POST"])
def create_menu_item():
    data = request.form.to_dict()  # text fields
    image = request.files.get("image")  # file
    image_path = save_uploaded_file(image) if image else None
    return add_menu_item(data, image_path)

# PUT update menu item with optional image
@menu_bp.route("/<id>", methods=["PUT"])
def update_menu_item(id):
    data = request.form.to_dict()
    image = request.files.get("image")
    image_path = save_uploaded_file(image) if image else None
    return edit_menu_item(id, data, image_path)

# DELETE menu item
@menu_bp.route("/<id>", methods=["DELETE"])
def remove_menu_item(id):
    return delete_menu_item(id)
