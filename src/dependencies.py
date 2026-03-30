from fastapi import Depends, HTTPException, Header
from typing import Optional, List
from auth import verificar_token, extrair_token_do_header, FuncionarioAuth

# Nícolas Bastos


async def get_current_active_user(authorization: Optional[str] = Header(None)) -> FuncionarioAuth:
    """
    Dependency: Verifica se o usuário está autenticado.
    Extrai o token do header Authorization e valida.
    Retorna o usuário autenticado.
    """
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        token = extrair_token_do_header(authorization)
        payload = verificar_token(token)
        
        # Verifica se é um token de acesso
        if payload.get("tipo") != "access":
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        usuario_id = payload.get("usuario_id")
        grupo = payload.get("grupo")
        
        if usuario_id is None or grupo is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return FuncionarioAuth(usuario_id=usuario_id, grupo=grupo, tipo_token="access")
    
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_group(grupos_permitidos: List[int]):
    """
    Factory function que retorna uma dependency para verificar se o usuário
    pertence a um dos grupos permitidos.
    
    Uso:
    current_user: FuncionarioAuth = Depends(require_group([1, 3]))
    """
    async def verificar_grupo(
        current_user: FuncionarioAuth = Depends(get_current_active_user),
    ) -> FuncionarioAuth:
        if current_user.grupo not in grupos_permitidos:
            raise HTTPException(
                status_code=403,
                detail=f"Acesso negado. Grupos permitidos: {grupos_permitidos}",
            )
        return current_user
    
    return verificar_grupo
