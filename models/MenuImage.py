from datetime import datetime

class MenuImage:
    def __init__(self, image_url):
        self.imageUrl = image_url
        self.uploadedAt = datetime.utcnow()
        self.createdAt = datetime.utcnow()  # same as timestamps in Mongoose
        self.updatedAt = datetime.utcnow()
    
    def to_dict(self):
        return {
            "imageUrl": self.imageUrl,
            "uploadedAt": self.uploadedAt,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
