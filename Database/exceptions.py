class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails"""
    pass

class AuthenticationError(DatabaseError):
    """Raised when authentication fails"""
    pass

class QueryError(DatabaseError):
    """Raised when database query fails"""
    pass