class APIError(Exception):
    """Base exception for API-related errors."""
    pass

class AuthenticationError(APIError):
    """Exception raised when authentication fails."""
    pass

class ResourceNotFoundError(APIError):
    """Exception raised when a requested resource is not found."""
    pass 