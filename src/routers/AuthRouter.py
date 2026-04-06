from fastapi import APIRouter, Depends, HTTPException, Request, status
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
from infra.rate_limit import limiter, limits
from security.auth import (
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    revoke_refresh_token,
    validate_refresh_token,
)
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.critical)
async def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    funcionario = (
        db.query(FuncionarioModel)
        .filter(
            (FuncionarioModel.matricula == payload.login)
            | (FuncionarioModel.cpf == payload.login)
        )
        .first()
    )
    if not funcionario or funcionario.senha != payload.senha:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=None,
            acao=AcaoAuditoria.LOGIN,
            recurso=RecursoAuditoria.AUTH,
            dados_novos={"login": payload.login, "sucesso": False},
        )
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais invalidas")

    access_token, access_expires = create_access_token(funcionario)
    refresh_token, _ = create_refresh_token(funcionario)

    AuditoriaService.registrar(
        db=db,
        request=request,
        funcionario_id=funcionario.id,
        acao=AcaoAuditoria.LOGIN,
        recurso=RecursoAuditoria.AUTH,
        recurso_id=funcionario.id,
        dados_novos={"login": payload.login, "sucesso": True},
    )
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_expires,
    )


@router.post("/refresh", response_model=AccessTokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def refresh_token(
    request: Request,
    payload: RefreshRequest,
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    _ = request
    token_payload = validate_refresh_token(payload.refresh_token)
    user_id = token_payload.get("sub")

    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == int(user_id)).first()
    if not funcionario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario nao encontrado")

    access_token, access_expires = create_access_token(funcionario)
    return AccessTokenResponse(access_token=access_token, expires_in=access_expires)


@router.get("/me", response_model=FuncionarioAuth, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def me(request: Request, current_user: FuncionarioAuth = Depends(get_current_active_user)) -> FuncionarioAuth:
    _ = request
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def logout(request: Request, payload: RefreshRequest) -> dict[str, str]:
    _ = request
    revoke_refresh_token(payload.refresh_token)
    return {"detail": "Logout realizado com sucesso"}
