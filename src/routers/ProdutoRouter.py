from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ProdutoSchema import (
    ProdutoCreate,
    ProdutoPublicResponse,
    ProdutoResponse,
    ProdutoUpdate,
)
from infra.database import get_db
from infra.orm.ProdutoModel import ProdutoModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user, require_group
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria
from services.QueryFilterService import (
    append_equal_filter,
    append_ilike_filter,
    append_range_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/produtos", tags=["Produto"])


def _produto_to_dict(produto: ProdutoModel) -> dict:
    return {
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "valor_unitario": produto.valor_unitario,
        "foto": bool(produto.foto),
    }


@router.get(
    "/publico",
    response_model=list[ProdutoPublicResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit(limits.low)
async def listar_produtos_publico(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[ProdutoModel]:
    _ = request
    statement = apply_pagination(select(ProdutoModel).order_by(ProdutoModel.id), skip=skip, limit=limit)
    result = await db.scalars(statement)
    return result.all()


@router.get("/", response_model=list[ProdutoResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_produtos(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    id: int | None = Query(None),
    nome: str | None = Query(None),
    descricao: str | None = Query(None),
    valor: float | None = Query(None),
    valor_min: float | None = Query(None),
    valor_max: float | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ProdutoModel]:
    _ = request
    _ = current_user

    if valor is not None and (valor_min is not None or valor_max is not None):
        raise HTTPException(
            status_code=400,
            detail="Use valor (igual) ou valor_min/valor_max (intervalo), nao ambos",
        )

    filters: list = []
    append_equal_filter(filters, ProdutoModel.id, id)
    append_ilike_filter(filters, ProdutoModel.nome, nome)
    append_ilike_filter(filters, ProdutoModel.descricao, descricao)
    append_range_filter(
        filters,
        ProdutoModel.valor_unitario,
        equal=valor,
        min_value=valor_min,
        max_value=valor_max,
    )

    statement = select(ProdutoModel).order_by(ProdutoModel.id)
    statement = apply_filters(statement, filters)
    statement = apply_pagination(statement, skip=skip, limit=limit)

    result = await db.scalars(statement)
    return result.all()


@router.get("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_produto_por_id(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ProdutoModel:
    _ = request
    _ = current_user
    produto = await db.scalar(select(ProdutoModel).where(ProdutoModel.id == id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return produto


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_produto(
    request: Request,
    payload: ProdutoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> ProdutoModel:
    _ = current_user
    produto = ProdutoModel(**payload.model_dump())
    try:
        db.add(produto)
        await db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.PRODUTO,
            recurso_id=produto.id,
            dados_novos=_produto_to_dict(produto),
        )
        await db.commit()
        await db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {exc}")


@router.put("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_produto(
    request: Request,
    id: int,
    payload: ProdutoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> ProdutoModel:
    _ = current_user
    produto = await db.scalar(select(ProdutoModel).where(ProdutoModel.id == id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    dados_antigos = _produto_to_dict(produto)

    dados = payload.model_dump(exclude_unset=True)
    try:
        for campo, valor in dados.items():
            setattr(produto, campo, valor)

        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.UPDATE,
            recurso=RecursoAuditoria.PRODUTO,
            recurso_id=produto.id,
            dados_antigos=dados_antigos,
            dados_novos=_produto_to_dict(produto),
        )

        await db.commit()
        await db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar produto: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_produto(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    produto = await db.scalar(select(ProdutoModel).where(ProdutoModel.id == id))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    dados_antigos = _produto_to_dict(produto)

    try:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.DELETE,
            recurso=RecursoAuditoria.PRODUTO,
            recurso_id=produto.id,
            dados_antigos=dados_antigos,
        )
        await db.delete(produto)
        await db.commit()
        return {"detail": "Produto removido com sucesso"}
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover produto: {exc}")