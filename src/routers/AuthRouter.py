from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from auth import criar_access_token, criar_refresh_token, verificar_token, extrair_token_do_header, FuncionarioAuth
from dependencies import get_current_active_user

# Nícolas Bastos

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    """Request para login com usuário e senha"""
    usuario_id: int
    senha: str
    grupo: int  # Simulação: normalmente viria do banco de dados


class TokenResponse(BaseModel):
    """Response com access token e refresh token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Request para refresh token"""
    refresh_token: str


class MeResponse(BaseModel):
    """Response com informações do usuário autenticado"""
    usuario_id: int
    grupo: int


# Endpoint de Login (público)
@router.post("/login", response_model=TokenResponse, status_code=200)
def login(credentials: LoginRequest):
    """
    Realiza login e retorna access token e refresh token.
    
    Neste exemplo, estamos aceitando qualquer combinação de usuario_id e senha.
    Em produção, você deve validar contra um banco de dados.
    """
    # Simulação: em produção, validar contra banco de dados
    if not credentials.usuario_id or not credentials.senha:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )
    
    access_token = criar_access_token(
        usuario_id=credentials.usuario_id,
        grupo=credentials.grupo
    )
    refresh_token = criar_refresh_token(
        usuario_id=credentials.usuario_id,
        grupo=credentials.grupo
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


# Endpoint de Refresh Token (público)
@router.post("/refresh", response_model=TokenResponse, status_code=200)
def refresh(request: RefreshRequest):
    """
    Usa um refresh token para gerar um novo access token e refresh token.
    """
    try:
        payload = verificar_token(request.refresh_token)
        
        # Verifica se é um token de refresh
        if payload.get("tipo") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Token inválido. Use um refresh token."
            )
        
        usuario_id = payload.get("usuario_id")
        grupo = payload.get("grupo")
        
        # Gera novos tokens
        access_token = criar_access_token(usuario_id=usuario_id, grupo=grupo)
        refresh_token = criar_refresh_token(usuario_id=usuario_id, grupo=grupo)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Erro ao renovar token: {str(e)}"
        )


# Endpoint de Informações do Usuário (autenticado)
@router.get("/me", response_model=MeResponse, status_code=200)
def get_me(current_user: FuncionarioAuth = Depends(get_current_active_user)):
    """
    Retorna informações do usuário autenticado.
    Requer header Authorization com access token.
    """
    return MeResponse(
        usuario_id=current_user.usuario_id,
        grupo=current_user.grupo
    )


# Endpoint de Logout (público)
@router.post("/logout", status_code=200)
def logout(authorization: Optional[str] = Header(None)):
    """
    Realiza logout.
    Em implementação real, você adicionaria o token a uma blacklist.
    """
    if not authorization:
        raise HTTPException(
            status_code=400,
            detail="Token não fornecido"
        )
    
    # Simulação: em produção, adicionar token à blacklist no Redis ou similar
    return {"detail": "Logout realizado com sucesso"}
