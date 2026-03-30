from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ClienteSchema import ClienteCreate, ClienteResponse, ClienteUpdate
from infra.database import get_db
from infra.orm.ClienteModel import ClienteModel
from security.auth import get_current_active_user, require_group

router = APIRouter(prefix="/clientes", tags=["Cliente"])


@router.get("/", response_model=list[ClienteResponse], status_code=status.HTTP_200_OK)
async def listar_clientes(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ClienteModel]:
    _ = current_user
    return db.query(ClienteModel).all()


@router.get("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
async def buscar_cliente_por_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ClienteModel:
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    payload: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
) -> ClienteModel:
    _ = current_user
    if db.query(ClienteModel).filter(ClienteModel.cpf == payload.cpf).first():
        raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    cliente = ClienteModel(**payload.model_dump())
    try:
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {exc}")


@router.put("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
async def atualizar_cliente(
    id: int,
    payload: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
) -> ClienteModel:
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    dados = payload.model_dump(exclude_unset=True)
    if "cpf" in dados:
        cpf_existente = (
            db.query(ClienteModel)
            .filter(ClienteModel.cpf == dados["cpf"], ClienteModel.id != id)
            .first()
        )
        if cpf_existente:
            raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    try:
        for campo, valor in dados.items():
            setattr(cliente, campo, valor)
        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cliente: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def remover_cliente(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    try:
        db.delete(cliente)
        db.commit()
        return {"detail": "Cliente removido com sucesso"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover cliente: {exc}")