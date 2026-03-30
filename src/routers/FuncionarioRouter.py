from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.schemas.FuncionarioSchema import (
    FuncionarioCreate,
    FuncionarioResponse,
    FuncionarioUpdate,
)
from domain.schemas.AuthSchema import FuncionarioAuth
from infra.database import get_db
from infra.orm.FuncionarioModel import FuncionarioModel
from security.auth import get_current_active_user, require_group

router = APIRouter(prefix="/funcionarios", tags=["Funcionario"])


@router.get("/", response_model=list[FuncionarioResponse], status_code=status.HTTP_200_OK)
async def listar_funcionarios(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> list[FuncionarioModel]:
    _ = current_user
    return db.query(FuncionarioModel).all()


@router.get("/{id}", response_model=FuncionarioResponse, status_code=status.HTTP_200_OK)
async def buscar_funcionario_por_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> FuncionarioModel:
    _ = current_user
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")
    return funcionario


@router.post("/", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_funcionario(
    payload: FuncionarioCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> FuncionarioModel:
    _ = current_user
    if db.query(FuncionarioModel).filter(FuncionarioModel.cpf == payload.cpf).first():
        raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    funcionario = FuncionarioModel(**payload.model_dump())
    try:
        db.add(funcionario)
        db.commit()
        db.refresh(funcionario)
        return funcionario
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar funcionario: {exc}")


@router.put("/{id}", response_model=FuncionarioResponse, status_code=status.HTTP_200_OK)
async def atualizar_funcionario(
    id: int,
    payload: FuncionarioUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> FuncionarioModel:
    _ = current_user
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")

    dados = payload.model_dump(exclude_unset=True)
    if "cpf" in dados:
        cpf_existente = (
            db.query(FuncionarioModel)
            .filter(FuncionarioModel.cpf == dados["cpf"], FuncionarioModel.id != id)
            .first()
        )
        if cpf_existente:
            raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    try:
        for campo, valor in dados.items():
            setattr(funcionario, campo, valor)
        db.commit()
        db.refresh(funcionario)
        return funcionario
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar funcionario: {exc}",
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def remover_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")

    try:
        db.delete(funcionario)
        db.commit()
        return {"detail": "Funcionario removido com sucesso"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover funcionario: {exc}")