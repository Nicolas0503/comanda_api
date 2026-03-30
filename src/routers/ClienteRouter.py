from fastapi import APIRouter, Depends
from domain.entities.Cliente import Cliente
from dependencies import get_current_active_user, require_group
from auth import FuncionarioAuth

#Nícolas Bastos

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

# GET TODOS - qualquer usuário autenticado
@router.get("/cliente/", tags=["Cliente"], status_code=200)
def get_cliente(current_user: FuncionarioAuth = Depends(get_current_active_user)):
    return {"msg": "cliente get todos executado", "usuario_id": current_user.usuario_id}

# GET UM - qualquer usuário autenticado
@router.get("/cliente/{id}", tags=["Cliente"], status_code=200)
def get_cliente(id: int, current_user: FuncionarioAuth = Depends(get_current_active_user)):
    return {"msg": "cliente get um executado", "usuario_id": current_user.usuario_id}

# POST - grupos 1 e 3
@router.post("/cliente/", tags=["Cliente"], status_code=200)
def post_cliente(corpo: Cliente, current_user: FuncionarioAuth = Depends(require_group([1, 3]))):
    return {"msg": "cliente post executado", "nome": corpo.nome, "cpf": corpo.cpf, "telefone": corpo.telefone, "usuario_id": current_user.usuario_id}

# PUT - grupos 1 e 3
@router.put("/cliente/{id}", tags=["Cliente"], status_code=200)
def put_cliente(id: int, corpo: Cliente, current_user: FuncionarioAuth = Depends(require_group([1, 3]))):
    return {"msg": "cliente put executado", "id":id, "nome": corpo.nome, "cpf": corpo.cpf, "telefone": corpo.telefone, "usuario_id": current_user.usuario_id}

# DELETE - apenas grupo 1
@router.delete("/cliente/{id}", tags=["Cliente"], status_code=200)
def delete_cliente(id: int, current_user: FuncionarioAuth = Depends(require_group([1]))):
    return {"msg": "cliente delete executado", "id":id, "usuario_id": current_user.usuario_id}