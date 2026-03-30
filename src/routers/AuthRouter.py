from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.AuthSchema import (
    AccessTokenResponse,
    FuncionarioAuth,
    LoginRequest,
    RefreshRequest,
    TokenResponse,
)
from infra.database import get_db
from infra.orm.FuncionarioModel import FuncionarioModel
from security.auth import (
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    revoke_refresh_token,
    validate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    funcionario = (
        db.query(FuncionarioModel)
        .filter(
            (FuncionarioModel.matricula == payload.login)
            | (FuncionarioModel.cpf == payload.login)
        )
        .first()
    )
    if not funcionario or funcionario.senha != payload.senha:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais invalidas")

    access_token, access_expires = create_access_token(funcionario)
    refresh_token, _ = create_refresh_token(funcionario)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_expires,
    )


@router.post("/refresh", response_model=AccessTokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)) -> AccessTokenResponse:
    token_payload = validate_refresh_token(payload.refresh_token)
    user_id = token_payload.get("sub")

    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == int(user_id)).first()
    if not funcionario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario nao encontrado")

    access_token, access_expires = create_access_token(funcionario)
    return AccessTokenResponse(access_token=access_token, expires_in=access_expires)


@router.get("/me", response_model=FuncionarioAuth, status_code=status.HTTP_200_OK)
async def me(current_user: FuncionarioAuth = Depends(get_current_active_user)) -> FuncionarioAuth:
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(payload: RefreshRequest) -> dict[str, str]:
    revoke_refresh_token(payload.refresh_token)
    return {"detail": "Logout realizado com sucesso"}
