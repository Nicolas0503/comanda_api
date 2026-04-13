from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ComandaSchema import (
    ComandaCreate,
    ComandaItemCreate,
    ComandaItemResponse,
    ComandaItemUpdate,
    ComandaProdutosResponse,
    ComandaResponse,
    ComandaUpdate,
)
from infra.database import get_db
from infra.orm.ComandaItemModel import ComandaItemModel
from infra.orm.ComandaModel import ComandaModel
from infra.orm.ProdutoModel import ProdutoModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user, require_group
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria
from services.QueryFilterService import (
    append_datetime_interval_filter,
    append_equal_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/comandas", tags=["Comanda"])


async def _buscar_comanda_por_numero(db: AsyncSession, numero: str) -> ComandaModel:
    comanda = await db.scalar(select(ComandaModel).where(ComandaModel.numero == numero))
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nao encontrada")
    return comanda


@router.get("/", response_model=list[ComandaResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_comandas(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    id: int | None = Query(None),
    numero: str | None = Query(None),
    status_comanda: str | None = Query(None, alias="status"),
    cliente_id: int | None = Query(None),
    funcionario_id: int | None = Query(None),
    data_inicio: datetime | None = Query(None),
    data_fim: datetime | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ComandaModel]:
    _ = request
    _ = current_user

    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(status_code=400, detail="data_inicio nao pode ser maior que data_fim")

    filters: list = []
    append_equal_filter(filters, ComandaModel.id, id)
    append_equal_filter(filters, ComandaModel.numero, numero)
    append_equal_filter(filters, ComandaModel.status, status_comanda)
    append_equal_filter(filters, ComandaModel.cliente_id, cliente_id)
    append_equal_filter(filters, ComandaModel.funcionario_id, funcionario_id)
    append_datetime_interval_filter(
        filters,
        ComandaModel.data_abertura,
        start_at=data_inicio,
        end_at=data_fim,
    )

    statement = select(ComandaModel).order_by(ComandaModel.data_abertura.desc())
    statement = apply_filters(statement, filters)
    statement = apply_pagination(statement, skip=skip, limit=limit)

    result = await db.scalars(statement)
    return result.all()


@router.get("/{id}", response_model=ComandaResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_comanda_por_id(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ComandaModel:
    _ = request
    _ = current_user

    comanda = await db.scalar(select(ComandaModel).where(ComandaModel.id == id))
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nao encontrada")
    return comanda


@router.post("/", response_model=ComandaResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_comanda(
    request: Request,
    payload: ComandaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2, 3])),
) -> ComandaModel:
    if await db.scalar(select(ComandaModel).where(ComandaModel.numero == payload.numero)):
        raise HTTPException(status_code=409, detail="Numero da comanda ja cadastrado")

    comanda = ComandaModel(**payload.model_dump())
    try:
        db.add(comanda)
        await db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.COMANDA,
            recurso_id=comanda.id,
            dados_novos={
                "id": comanda.id,
                "numero": comanda.numero,
                "status": comanda.status,
                "cliente_id": comanda.cliente_id,
                "funcionario_id": comanda.funcionario_id,
            },
        )
        await db.commit()
        await db.refresh(comanda)
        return comanda
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar comanda: {exc}")


@router.put("/{id}", response_model=ComandaResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_comanda(
    request: Request,
    id: int,
    payload: ComandaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2, 3])),
) -> ComandaModel:
    comanda = await db.scalar(select(ComandaModel).where(ComandaModel.id == id))
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nao encontrada")

    dados = payload.model_dump(exclude_unset=True)
    if "numero" in dados:
        numero_existente = await db.scalar(
            select(ComandaModel).where(ComandaModel.numero == dados["numero"], ComandaModel.id != id)
        )
        if numero_existente:
            raise HTTPException(status_code=409, detail="Numero da comanda ja cadastrado")

    dados_antigos = {
        "id": comanda.id,
        "numero": comanda.numero,
        "status": comanda.status,
        "cliente_id": comanda.cliente_id,
        "funcionario_id": comanda.funcionario_id,
    }

    try:
        for campo, valor in dados.items():
            setattr(comanda, campo, valor)

        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.UPDATE,
            recurso=RecursoAuditoria.COMANDA,
            recurso_id=comanda.id,
            dados_antigos=dados_antigos,
            dados_novos={
                "id": comanda.id,
                "numero": comanda.numero,
                "status": comanda.status,
                "cliente_id": comanda.cliente_id,
                "funcionario_id": comanda.funcionario_id,
            },
        )
        await db.commit()
        await db.refresh(comanda)
        return comanda
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar comanda: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_comanda(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2])),
) -> dict[str, str]:
    comanda = await db.scalar(select(ComandaModel).where(ComandaModel.id == id))
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nao encontrada")

    dados_antigos = {
        "id": comanda.id,
        "numero": comanda.numero,
        "status": comanda.status,
        "cliente_id": comanda.cliente_id,
        "funcionario_id": comanda.funcionario_id,
    }

    try:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.DELETE,
            recurso=RecursoAuditoria.COMANDA,
            recurso_id=comanda.id,
            dados_antigos=dados_antigos,
        )
        await db.delete(comanda)
        await db.commit()
        return {"detail": "Comanda removida com sucesso"}
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover comanda: {exc}")


@router.post("/numero/{numero}/itens", response_model=ComandaItemResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def adicionar_item_na_comanda(
    request: Request,
    numero: str,
    payload: ComandaItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2, 3])),
) -> ComandaItemResponse:
    comanda = await _buscar_comanda_por_numero(db, numero)
    produto = await db.scalar(select(ProdutoModel).where(ProdutoModel.id == payload.produto_id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    if payload.quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    item = ComandaItemModel(
        comanda_id=comanda.id,
        produto_id=payload.produto_id,
        quantidade=payload.quantidade,
    )
    try:
        db.add(item)
        await db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.COMANDA_ITEM,
            recurso_id=item.id,
            dados_novos={
                "comanda_numero": comanda.numero,
                "item_id": item.id,
                "produto_id": item.produto_id,
                "quantidade": item.quantidade,
            },
        )
        await db.commit()
        return ComandaItemResponse(
            item_id=item.id,
            produto_id=produto.id,
            produto_nome=produto.nome,
            produto_descricao=produto.descricao,
            quantidade=item.quantidade,
        )
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar item na comanda: {exc}")


@router.put("/numero/{numero}/itens/{item_id}", response_model=ComandaItemResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_quantidade_item_comanda(
    request: Request,
    numero: str,
    item_id: int,
    payload: ComandaItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2, 3])),
) -> ComandaItemResponse:
    comanda = await _buscar_comanda_por_numero(db, numero)
    item = await db.scalar(
        select(ComandaItemModel).where(
            ComandaItemModel.id == item_id,
            ComandaItemModel.comanda_id == comanda.id,
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item da comanda nao encontrado")
    if payload.quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    produto = await db.scalar(select(ProdutoModel).where(ProdutoModel.id == item.produto_id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    quantidade_antiga = item.quantidade
    try:
        item.quantidade = payload.quantidade
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.UPDATE,
            recurso=RecursoAuditoria.COMANDA_ITEM,
            recurso_id=item.id,
            dados_antigos={"quantidade": quantidade_antiga},
            dados_novos={"quantidade": item.quantidade},
        )
        await db.commit()
        return ComandaItemResponse(
            item_id=item.id,
            produto_id=produto.id,
            produto_nome=produto.nome,
            produto_descricao=produto.descricao,
            quantidade=item.quantidade,
        )
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar item da comanda: {exc}")


@router.delete("/numero/{numero}/itens/{item_id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_item_comanda(
    request: Request,
    numero: str,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 2, 3])),
) -> dict[str, str]:
    comanda = await _buscar_comanda_por_numero(db, numero)
    item = await db.scalar(
        select(ComandaItemModel).where(
            ComandaItemModel.id == item_id,
            ComandaItemModel.comanda_id == comanda.id,
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item da comanda nao encontrado")

    try:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.DELETE,
            recurso=RecursoAuditoria.COMANDA_ITEM,
            recurso_id=item.id,
            dados_antigos={
                "comanda_numero": comanda.numero,
                "produto_id": item.produto_id,
                "quantidade": item.quantidade,
            },
        )
        await db.delete(item)
        await db.commit()
        return {"detail": "Item removido da comanda com sucesso"}
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover item da comanda: {exc}")


@router.get("/numero/{numero}/itens", response_model=ComandaProdutosResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_itens_da_comanda(
    request: Request,
    numero: str,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ComandaProdutosResponse:
    _ = request
    _ = current_user
    comanda = await _buscar_comanda_por_numero(db, numero)

    rows = await db.execute(
        select(ComandaItemModel, ProdutoModel)
        .join(ProdutoModel, ProdutoModel.id == ComandaItemModel.produto_id)
        .where(ComandaItemModel.comanda_id == comanda.id)
        .order_by(ComandaItemModel.id)
    )

    itens = [
        ComandaItemResponse(
            item_id=item.id,
            produto_id=produto.id,
            produto_nome=produto.nome,
            produto_descricao=produto.descricao,
            quantidade=item.quantidade,
        )
        for item, produto in rows.all()
    ]
    return ComandaProdutosResponse(comanda_id=comanda.id, comanda_numero=comanda.numero, itens=itens)
