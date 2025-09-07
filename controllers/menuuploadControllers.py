from flask import jsonify
from bson import ObjectId
from config.db import db
import cloudinary  # the package is already configured  # ✅ use this object
from datetime import datetime

images_collection = db["menuimages"]

# =======================
# 📌 Get all Menu Images
# =======================
def get_menu_images():
    try:
        images = list(images_collection.find().sort("createdAt", -1))
        for img in images:
            img["_id"] = str(img["_id"])
        return jsonify(images), 200
    except Exception as e:
        return jsonify({"message": "Error fetching menu images", "error": str(e)}), 500


# =======================
# 📌 Upload Menu Image
# =======================
def upload_menu_image(file):
    try:
        if not file:
            return jsonify({"message": "No file uploaded"}), 400

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(file, folder="menu_images")  # ✅ fixed

        # Save in DB
        new_image = {
            "imageUrl": result.get("secure_url"),
            "createdAt": datetime.utcnow()
        }
        inserted = images_collection.insert_one(new_image)
        new_image["_id"] = str(inserted.inserted_id)

        return jsonify(new_image), 201
    except Exception as e:
        return jsonify({"message": "Error uploading menu image", "error": str(e)}), 500


# =======================
# 📌 Delete Menu Image
# =======================
def delete_menu_image(id):
    try:
        image = images_collection.find_one({"_id": ObjectId(id)})
        if not image:
            return jsonify({"message": "Menu image not found"}), 404

        # Extract public_id (folder/filename without extension)
        public_id = "/".join(image["imageUrl"].split("/")[-2:]).split(".")[0]

        # Delete from Cloudinary
        cloudinary.uploader.destroy(public_id)  # ✅ fixed

        # Delete from DB
        images_collection.delete_one({"_id": ObjectId(id)})

        return jsonify({"message": "Menu image deleted successfully"})
    except Exception as e:
        return jsonify({"message": "Error deleting menu image", "error": str(e)}), 500
