class TokenData:
    """
    Data model for token payload.
    This model is used to define the structure of the data contained in the JWT token.
    """

    sub: str  # Subject (usually user ID)
    exp: int  # Expiration time (timestamp)
    iat: int  # Issued at time (timestamp)
    role: str  # User role
    is_active: bool  # User active status
