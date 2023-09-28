from fastapi import APIRouter, Depends

from models.admin_tools import CreateUserRequest
from models.auth import AuthCheckEmailRequest, AuthCheckEmailResponse, SignInRequest, TokenResponse, SetPasswordRequest, ChangePasswordRequest
from models.users import UserOut
from value_types import ProfileType
from services import users, auth, jwt
from routes.middlewares import get_facade_services_if_authenticated
from services.facade import Services
import exceptions


router = APIRouter(prefix="/auth", tags=['auth'])



@router.post("/check_email", response_model=AuthCheckEmailResponse,
             responses=exceptions.make_schemas(exceptions.USER_NOT_FOUND))
async def check_email(req: AuthCheckEmailRequest):
    user = await users.get_user_by(email=req.email)
    return AuthCheckEmailResponse(email=user.email, has_password=user.is_activated())


#вводим email и password в ответ вернем token и данные usera
@router.post("/sign_in", response_model=TokenResponse,
             responses=exceptions.make_schemas(exceptions.USER_HAS_NO_PASSWORD, exceptions.USER_NOT_FOUND, exceptions.INVALID_PASSWORD))
async def sign_in(body: SignInRequest):
    user = await auth.authenticate(body.email, body.password)#проверяем имеется ли пользователь в базе
    return TokenResponse(token=await jwt.issue_jwt_token(user.id), user=await UserOut.from_tortoise_orm(user))#возврашает сгенерированный токен по айди и информации юзера

#получаем email существуешего партнера или инженера и если не имеет пароля то создаем для него пароль
@router.post("/set_password", response_model=TokenResponse,
             responses=exceptions.make_schemas(exceptions.USER_ALREADY_SET_PASSWORD, exceptions.USER_NOT_FOUND))
async def set_initial_password(body: SetPasswordRequest):
    user = await users.set_password(body.email, body.password)
    return TokenResponse(token=await jwt.issue_jwt_token(user.id), user=await UserOut.from_tortoise_orm(user))


@router.post("/change_password", responses=exceptions.make_schemas(exceptions.PASSWORDS_DO_NOT_MATCH))
async def change_password(body: ChangePasswordRequest,
                          services: Services = Depends(get_facade_services_if_authenticated)):
    return await auth.change_password(services.user, body.password, body.password_cnf)