from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # enable CORS
app.config["JSON_SORT_KEYS"] = False  # keeps JSON in original order

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["viscountiEu"]   # change "restaurantDB" to your actual DB name

print("✅ MongoDB connected")

# Import Blueprints (like Express routes)
from Routes.MenuRoutes import menu_bp
from Routes.imageRoutes import image_bp
from Routes.offerBadgeRoutes import offer_badge_bp

# Register routes
app.register_blueprint(menu_bp, url_prefix="/api/menu")
app.register_blueprint(image_bp, url_prefix="/api")
app.register_blueprint(offer_badge_bp, url_prefix="/api/offer-badges")

# Run locally (PythonAnywhere uses WSGI instead)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
