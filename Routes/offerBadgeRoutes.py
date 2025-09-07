from flask import Blueprint, request, jsonify
from controllers.offerBadgeController import get_badges, add_badge, delete_badge

offer_badge_bp = Blueprint("offer_badge", __name__)

# GET all badges
@offer_badge_bp.route("/", methods=["GET"])
def get_all_badges():
    return get_badges()

# POST new badge
@offer_badge_bp.route("/", methods=["POST"])
def create_badge():
    data = request.get_json()
    return add_badge(data)

# DELETE badge
@offer_badge_bp.route("/<id>", methods=["DELETE"])
def remove_badge(id):
    return delete_badge(id)
