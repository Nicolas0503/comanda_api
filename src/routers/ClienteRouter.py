from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ClienteSchema import ClienteCreate, ClienteResponse, ClienteUpdate
from infra.database import get_db
from infra.orm.ClienteModel import ClienteModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user, require_group
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria
from services.QueryFilterService import (
    append_equal_filter,
    append_ilike_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/clientes", tags=["Cliente"])


def _cliente_to_dict(cliente: ClienteModel) -> dict:
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "telefone": cliente.telefone,
    }


@router.get("/", response_model=list[ClienteResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_clientes(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    id: int | None = Query(None),
    nome: str | None = Query(None),
    cpf: str | None = Query(None),
    telefone: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ClienteModel]:
    _ = request
    _ = current_user

    filters: list = []
    append_equal_filter(filters, ClienteModel.id, id)
    append_ilike_filter(filters, ClienteModel.nome, nome)
    append_equal_filter(filters, ClienteModel.cpf, cpf)
    append_equal_filter(filters, ClienteModel.telefone, telefone)

    statement = select(ClienteModel).order_by(ClienteModel.id)
    statement = apply_filters(statement, filters)
    statement = apply_pagination(statement, skip=skip, limit=limit)

    result = await db.scalars(statement)
    return result.all()


@router.get("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_cliente_por_id(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ClienteModel:
    _ = request
    _ = current_user
    cliente = await db.scalar(select(ClienteModel).where(ClienteModel.id == id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_cliente(
    request: Request,
    payload: ClienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
) -> ClienteModel:
    _ = current_user
    if await db.scalar(select(ClienteModel).where(ClienteModel.cpf == payload.cpf)):
        raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    cliente = ClienteModel(**payload.model_dump())
    try:
        db.add(cliente)
        await db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.CLIENTE,
            recurso_id=cliente.id,
            dados_novos=_cliente_to_dict(cliente),
        )
        await db.commit()
        await db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {exc}")


@router.put("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_cliente(
    request: Request,
    id: int,
    payload: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
) -> ClienteModel:
    _ = current_user
    cliente = await db.scalar(select(ClienteModel).where(ClienteModel.id == id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    dados_antigos = _cliente_to_dict(cliente)

    dados = payload.model_dump(exclude_unset=True)
    if "cpf" in dados:
        cpf_existente = (
            await db.scalar(
                select(ClienteModel).where(
                    ClienteModel.cpf == dados["cpf"],
                    ClienteModel.id != id,
                )
            )
        )
        if cpf_existente:
            raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    try:
        for campo, valor in dados.items():
            setattr(cliente, campo, valor)

        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.UPDATE,
            recurso=RecursoAuditoria.CLIENTE,
            recurso_id=cliente.id,
            dados_antigos=dados_antigos,
            dados_novos=_cliente_to_dict(cliente),
        )

        await db.commit()
        await db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cliente: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_cliente(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    cliente = await db.scalar(select(ClienteModel).where(ClienteModel.id == id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    dados_antigos = _cliente_to_dict(cliente)

    try:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.DELETE,
            recurso=RecursoAuditoria.CLIENTE,
            recurso_id=cliente.id,
            dados_antigos=dados_antigos,
        )
        await db.delete(cliente)
        await db.commit()
        return {"detail": "Cliente removido com sucesso"}
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover cliente: {exc}")