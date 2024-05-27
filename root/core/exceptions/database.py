
class ItemNotFound(Exception):
    """Exception raised when an item is not found."""
    def __str__(self):
        return {"message": str(self), "data": self.data}

    def dict(self):
        return {
            "error": "UID not found",
            "message": "The provided UID does not exist. Please check the UID and try again."
        }
