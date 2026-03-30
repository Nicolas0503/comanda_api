from fastapi import APIRouter, Depends
from typing import Optional
from domain.entities.Produto import Produto
from dependencies import get_current_active_user, require_group
from auth import FuncionarioAuth

#Nícolas Bastos

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

# GET TODOS (público - sem autenticação) - lista simples sem id e valor
@router.get("/produto/publico", tags=["Produto"], status_code=200)
def get_produto_publico():
    return {"msg": "produto get todos (público) executado"}

# GET TODOS (autenticado) - lista completa
@router.get("/produto/", tags=["Produto"], status_code=200)
def get_produto(current_user: FuncionarioAuth = Depends(get_current_active_user)):
    return {"msg": "produto get todos (completo) executado", "usuario_id": current_user.usuario_id}

# GET UM - autenticado
@router.get("/produto/{id}", tags=["Produto"], status_code=200)
def get_produto(id: int, current_user: FuncionarioAuth = Depends(get_current_active_user)):
    return {"msg": "produto get um executado", "usuario_id": current_user.usuario_id}

# POST - grupo 1
@router.post("/produto/", tags=["Produto"], status_code=200)
def post_produto(corpo: Produto, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "produto post executado", "nome": corpo.nome, "descricao": corpo.descricao, "foto": corpo.foto, "valor_unitario": corpo.valor_unitario, "usuario_id": current_user.usuario_id}

# PUT - grupo 1
@router.put("/produto/{id}", tags=["Produto"], status_code=200)
def put_produto(id: int, corpo: Produto, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "produto put executado", "id": id, "nome": corpo.nome, "descricao": corpo.descricao, "foto": corpo.foto, "valor_unitario": corpo.valor_unitario, "usuario_id": current_user.usuario_id}

# DELETE - grupo 1
@router.delete("/produto/{id}", tags=["Produto"], status_code=200)
def delete_produto(id: int, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "produto delete executado", "id": id, "usuario_id": current_user.usuario_id}