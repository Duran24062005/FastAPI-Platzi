class AppException(Exception):
    def __init__(self, detail: str, status_code: int) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail=detail, status_code=404)


class ValidationAppError(AppException):
    def __init__(self, detail: str = "Validation error") -> None:
        super().__init__(detail=detail, status_code=400)


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(detail=detail, status_code=401)


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(detail=detail, status_code=403)


class ConflictError(AppException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(detail=detail, status_code=409)
