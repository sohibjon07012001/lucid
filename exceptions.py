import typing

from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic import BaseModel, Field


class APIExceptionModel(BaseModel):
    detail: str = Field(..., description="Сообщение об ошибке")


class APIException(HTTPException):
    model: APIExceptionModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = APIExceptionModel(detail=self.detail)

    def schema(self):
        return {
            'model': self.model.__class__,
            'content': {
                'application/json': {
                    'example': {'detail': self.detail},
                }
            },
        }

    def format(self, *args, **kwargs):
        self.detail = self.detail.format(*args, **kwargs)
        return self


def make_schemas(*args):
    d = {}
    for arg in args:
        if isinstance(arg, APIException):
            d[arg.status_code] = arg.schema()
    return d



USER_NOT_FOUND = APIException(404, "User not found")
USER_HAS_NO_PASSWORD  = APIException(206, "User has no password")
USER_ALREADY_SET_PASSWORD = APIException(409, "User already has a password")
INVALID_PASSWORD = APIException(401, "Invalid email/password")
NOT_AUTHENTICATED = APIException(401, "Not authenticated")
FORBIDDEN = APIException(403, "Forbidden")
PARTNER_NOT_FOUND = APIException(404, "Partner not found")
PASSWORDS_DO_NOT_MATCH = APIException(422, "Passwords do not match")