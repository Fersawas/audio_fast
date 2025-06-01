from fastapi import status, HTTPException

UserExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists"
)


class MainException(Exception):
    pass


class UserNotFoundException(MainException):
    pass


class JWTException(MainException):
    pass


class ExpitedTokenException(MainException):
    pass


class PasswordNotMatchException(MainException):
    pass
