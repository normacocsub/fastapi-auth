from fastapi import HTTPException, Depends
from typing import List
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth import verify_token
from jose import JWTError

security_schema = HTTPBearer()
oauth2_scheme = HTTPBearer(scheme_name="Bearer")


def has_permission(roles: List[str], allowed_roles: List[str]) -> bool:
    for role in roles:
        if role in allowed_roles:
            return True
    return False


def auth_required(roles=None):
    async def wrapper(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        try:
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid Token")
            user_roles = payload.get("role")
            if not has_permission(user_roles, roles):
                raise HTTPException(status_code=401, detail="El usuario no tiene permisos")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token Invalid")
    return wrapper

