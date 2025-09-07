from flask import jsonify, request
from bson import ObjectId
from config.db import db
from datetime import datetime, timezone

badges_collection = db["offerbadges"]

# ---------------- GET ALL BADGES ----------------
def get_badges():
    try:
        badges = list(badges_collection.find().sort("createdAt", -1))
        for badge in badges:
            badge["_id"] = str(badge["_id"])
        return jsonify(badges), 200
    except Exception as e:
        return jsonify({"message": "Error fetching badges", "error": str(e)}), 500

# ---------------- ADD NEW BADGE ----------------
def add_badge(data):
    try:
        print("Received data:", data)  # Debug input
        
        title = data.get("title")
        description = data.get("description")
        discount = data.get("discount")
        expiry_date = data.get("expiryDate")  # Expecting ISO string or date string

        # Debug extracted values
        print(f"title: {title}, description: {description}, discount: {discount}, expiryDate: {expiry_date}")

        # Validate required fields
        if not title or not discount:
            print("Validation failed: missing title or discount")  # Debug validation
            return jsonify({"message": "Title and discount are required"}), 400

        new_badge = {
            "title": title,
            "description": description,
            "discount": discount,
            "expiryDate": expiry_date,
            "createdAt": datetime.now(timezone.utc)
        }

        print("Inserting new badge into DB:", new_badge)  # Debug before DB insert
        inserted = badges_collection.insert_one(new_badge)
        new_badge["_id"] = str(inserted.inserted_id)
        print("Inserted badge ID:", new_badge["_id"])  # Debug inserted ID

        return jsonify(new_badge), 201

    except Exception as e:
        print("Error occurred while adding badge:", str(e))  # Debug exception
        return jsonify({"message": "Error adding badge", "error": str(e)}), 500

# ---------------- DELETE BADGE ----------------
def delete_badge(id):
    try:
        deleted = badges_collection.find_one_and_delete({"_id": ObjectId(id)})
        if not deleted:
            return jsonify({"message": "Badge not found"}), 404
        deleted["_id"] = str(deleted["_id"])
        return jsonify({"message": "Badge deleted successfully", "deletedBadge": deleted})
    except Exception as e:
        return jsonify({"message": "Error deleting badge", "error": str(e)}), 500
