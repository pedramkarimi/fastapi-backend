from typing import Any, Dict, Optional
from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        self.extra = extra or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "status_code": self.status_code,
            "code": self.code,
            "extra": self.extra,
        }


# --------- Auth Exceptions ---------

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_CREDENTIALS",
        )


class TokenExpiredException(AppException):
    def __init__(self, message: str = "Token has expired") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_EXPIRED",
        )


class TokenInvalidException(AppException):
    def __init__(self, message: str = "Token is invalid") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_INVALID",
        )


class PermissionDeniedException(AppException):
    def __init__(self, message: str = "You do not have permission") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            code="AUTH_PERMISSION_DENIED",
        )


class TooManyRequestsException(AppException):
    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="AUTH_TOO_MANY_REQUESTS",
        )


# --------- Common Exceptions ---------

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code="COMMON_NOT_FOUND",
        )


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code="COMMON_CONFLICT",
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", *, extra=None) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="COMMON_VALIDATION_ERROR",
            extra=extra,
        )
