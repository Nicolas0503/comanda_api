from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel
from settings import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# Nícolas Bastos

class TokenPayload(BaseModel):
    """Payload do token JWT"""
    usuario_id: int
    grupo: int
    tipo: str  # "access" ou "refresh"


class FuncionarioAuth(BaseModel):
    """Modelo de usuário autenticado"""
    usuario_id: int
    grupo: int
    tipo_token: str


def criar_access_token(usuario_id: int, grupo: int) -> str:
    """
    Cria um access token JWT com validade de 15 minutos
    """
    agora = datetime.utcnow()
    expiracao = agora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "usuario_id": usuario_id,
        "grupo": grupo,
        "tipo": "access",
        "iat": agora,
        "exp": expiracao
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def criar_refresh_token(usuario_id: int, grupo: int) -> str:
    """
    Cria um refresh token JWT com validade de 7 dias
    """
    agora = datetime.utcnow()
    expiracao = agora + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "usuario_id": usuario_id,
        "grupo": grupo,
        "tipo": "refresh",
        "iat": agora,
        "exp": expiracao
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verificar_token(token: str) -> dict:
    """
    Verifica e decodifica um token JWT.
    Retorna o payload se válido.
    Lança exceção se inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")


def extrair_token_do_header(authorization_header: str) -> str:
    """
    Extrai o token do header Authorization: Bearer <token>
    """
    if not authorization_header:
        raise Exception("Header Authorization não fornecido")
    
    partes = authorization_header.split()
    
    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise Exception("Formato de Authorization inválido. Use: Bearer <token>")
    
    return partes[1]
