from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from app.config import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.USER_KEY, settings.USER_ALGORITM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user