from datetime import datetime

class MenuItem:
    # Allowed categories (like Mongoose enum)
    allowed_categories = [
        "menu fisso",
        "pizze-tradizionali",
        "pizze-speciali",
        "calzoni",
        "kebab-panini",
        "burgers",
        "bibite",
        "fritte",
        "Indian cuisine",
        "dolco"
    ]

    def __init__(self, category, name, description, price, image, available=True):
        if category not in self.allowed_categories:
            raise ValueError(f"Invalid category. Allowed: {self.allowed_categories}")
        
        self.category = category
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.available = available
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "available": self.available,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
