from datetime import datetime

class OfferBadge:
    def __init__(self, title, discount, expiry_date, description="", is_active=True):
        if not title or discount is None or not expiry_date:
            raise ValueError("Title, discount, and expiryDate are required")

        self.title = title.strip()
        self.description = description.strip()
        self.discount = discount  # percentage, e.g., 20
        self.expiryDate = expiry_date  # datetime object or ISO string
        self.isActive = is_active
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "discount": self.discount,
            "expiryDate": self.expiryDate,
            "isActive": self.isActive,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
