import jwt
import datetime
import uuid

import config


async def issue_jwt_token(user_id: uuid.UUID) -> str:
    """Выпуск JWT токена по UUID пользователя"""
    return jwt.encode(
        {'exp': datetime.datetime.now() + datetime.timedelta(seconds=config.JWT.EXPIRY),
         'sub': str(user_id),
         },
        config.JWT.SECRET
    )