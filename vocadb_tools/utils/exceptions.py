import sys

class VocaDBAPIError(Exception):
    """Exception raised for errors in the VocaDB API."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        sys.exit(1)  # Exit the program with status code 1