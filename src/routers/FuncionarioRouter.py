from fastapi import APIRouter, Depends
from domain.entities.Funcionario import Funcionario
from dependencies import get_current_active_user, require_group
from auth import FuncionarioAuth

#Nícolas Bastos

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

# GET TODOS - apenas grupo 1 (admin)
@router.get("/funcionario/", tags=["Funcionário"], status_code=200)
def get_funcionario(current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "funcionario get todos executado", "usuario_id": current_user.usuario_id}

# GET UM - qualquer usuário autenticado
@router.get("/funcionario/{id}", tags=["Funcionário"], status_code=200)
def get_funcionario(id: int, current_user: FuncionarioAuth = Depends(get_current_active_user)):
    return {"msg": "funcionario get um executado", "usuario_id": current_user.usuario_id}

# POST - apenas grupo 1
@router.post("/funcionario/", tags=["Funcionário"], status_code=200)
def post_funcionario(corpo: Funcionario, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "funcionario post executado", "nome": corpo.nome, "cpf": corpo.cpf, "telefone": corpo.telefone, "usuario_id": current_user.usuario_id}

# PUT - apenas grupo 1
@router.put("/funcionario/{id}", tags=["Funcionário"], status_code=200)
def put_funcionario(id: int, corpo: Funcionario, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "funcionario put executado", "id": id, "nome": corpo.nome, "cpf": corpo.cpf, "telefone": corpo.telefone, "usuario_id": current_user.usuario_id}

# DELETE - apenas grupo 1
@router.delete("/funcionario/{id}", tags=["Funcionário"], status_code=200)
def delete_funcionario(id: int, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "funcionario delete executado", "id":id, "usuario_id": current_user.usuario_id}