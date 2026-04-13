from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuthSchema import FuncionarioAuth
from infra.database import get_db
from infra.orm.FuncionarioModel import FuncionarioModel
from settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


bearer_scheme = HTTPBearer(auto_error=True)

# In-memory revocation for refresh tokens during process lifetime.
revoked_refresh_jti: set[str] = set()


def _create_token(payload: dict, expires_delta: timedelta, token_type: str) -> str:
    data = payload.copy()
    expire = datetime.now(UTC) + expires_delta
    data.update({"exp": expire, "type": token_type, "jti": str(uuid4())})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_access_token(user: FuncionarioModel) -> tuple[str, int]:
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = _create_token(
        {
            "sub": str(user.id),
            "grupo": str(user.grupo),
        },
        expires,
        token_type="access",
    )
    return token, ACCESS_TOKEN_EXPIRE_MINUTES * 60


def create_refresh_token(user: FuncionarioModel) -> tuple[str, int]:
    expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = _create_token(
        {
            "sub": str(user.id),
            "grupo": str(user.grupo),
        },
        expires,
        token_type="refresh",
    )
    return token, REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> FuncionarioAuth:
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sem usuario",
            headers={"WWW-Authenticate": "Bearer"},
        )

    funcionario = await db.scalar(select(FuncionarioModel).where(FuncionarioModel.id == int(user_id)))
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return FuncionarioAuth.model_validate(funcionario)


def require_group(groups: list[int]) -> Callable:
    allowed = {str(group) for group in groups}

    def _dependency(current_user: FuncionarioAuth = Depends(get_current_active_user)) -> FuncionarioAuth:
        if str(current_user.grupo) not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sem permissao para este recurso",
            )
        return current_user

    return _dependency


def revoke_refresh_token(refresh_token: str) -> None:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token invalido")

    jti = payload.get("jti")
    if jti:
        revoked_refresh_jti.add(jti)


def validate_refresh_token(refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token invalido")

    jti = payload.get("jti")
    if jti and jti in revoked_refresh_jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revogado")

    return payload
