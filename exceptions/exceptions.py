from fastapi import status, HTTPException

UserExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists"
)


class UserNotFoundException(Exception):
    pass


class JWTException(Exception):
    pass


class ExpitedTokenException(Exception):
    pass
