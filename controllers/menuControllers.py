from flask import jsonify
from bson import ObjectId
from config.db import db
import cloudinary
import cloudinary.uploader  # ✅ required for uploads
import cloudinary.api       # optional for API calls

menu_collection = db["menuitems"]  # make sure this matches your MongoDB collection

# ---------------- GET ALL ----------------
def get_all_menu_items():
    try:
        menu_items = list(menu_collection.find())
        print(f"[DEBUG] Fetched {len(menu_items)} items from MongoDB")

        # Group items by category
        grouped_items = {}
        for item in menu_items:
            print(f"[DEBUG] Processing item: {item}")  # log each item
            category = item.get("category", "uncategorized")
            item["_id"] = str(item["_id"])
            grouped_items.setdefault(category, []).append(item)
            print(f"[DEBUG] Grouped items so far: {grouped_items}")

        print(f"[DEBUG] Final grouped items: {grouped_items}")
        return jsonify({"groupedItems": grouped_items}), 200

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        return jsonify({"message": "Error fetching menu items", "error": str(e)}), 500


# ---------------- ADD ----------------
def add_menu_item(data, file=None):
    try:
        image_url = ""
        if file:
            try:
                print(f"[DEBUG] Uploading file to Cloudinary: {file.filename if hasattr(file, 'filename') else file}")
                result = cloudinary.uploader.upload(file)
                image_url = result.get("secure_url", "")
                print(f"[DEBUG] Upload successful, URL: {image_url}")
            except Exception as e:
                print(f"[ERROR] Cloudinary upload failed: {str(e)}")
                return jsonify({"message": "Error uploading menu image", "error": str(e)}), 500

        new_item = {
            "category": data.get("category"),
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "image": image_url
        }
        inserted = menu_collection.insert_one(new_item)
        new_item["_id"] = str(inserted.inserted_id)
        return jsonify(new_item), 201

    except Exception as e:
        print(f"[ERROR] Failed to add menu item: {str(e)}")
        return jsonify({"message": "Error adding menu item", "error": str(e)}), 500


# ---------------- EDIT ----------------
def edit_menu_item(id, data, file=None):
    try:
        update_data = {
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "category": data.get("category"),
        }

        if file:
            try:
                print(f"[DEBUG] Uploading file to Cloudinary for edit: {file.filename if hasattr(file, 'filename') else file}")
                result = cloudinary.uploader.upload(file)
                update_data["image"] = result.get("secure_url")
                print(f"[DEBUG] Upload successful, URL: {update_data['image']}")
            except Exception as e:
                print(f"[ERROR] Cloudinary upload failed during edit: {str(e)}")
                return jsonify({"message": "Error uploading menu image", "error": str(e)}), 500

        updated = menu_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        if not updated:
            return jsonify({"message": "Menu item not found"}), 404
        updated["_id"] = str(updated["_id"])
        return jsonify(updated)

    except Exception as e:
        print(f"[ERROR] Failed to edit menu item: {str(e)}")
        return jsonify({"message": "Error updating menu item", "error": str(e)}), 500


# ---------------- DELETE ----------------
def delete_menu_item(id):
    try:
        deleted = menu_collection.find_one_and_delete({"_id": ObjectId(id)})
        if not deleted:
            return jsonify({"message": "Menu item not found"}), 404
        deleted["_id"] = str(deleted["_id"])
        return jsonify({"message": "Menu item deleted", "deletedItem": deleted})

    except Exception as e:
        print(f"[ERROR] Failed to delete menu item: {str(e)}")
        return jsonify({"message": "Error deleting menu item", "error": str(e)}), 500
