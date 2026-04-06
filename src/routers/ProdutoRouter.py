from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

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
async def listar_produtos_publico(request: Request, db: Session = Depends(get_db)) -> list[ProdutoModel]:
    _ = request
    return db.query(ProdutoModel).all()


@router.get("/", response_model=list[ProdutoResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_produtos(
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ProdutoModel]:
    _ = request
    _ = current_user
    return db.query(ProdutoModel).all()


@router.get("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_produto_por_id(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ProdutoModel:
    _ = request
    _ = current_user
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return produto


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_produto(
    request: Request,
    payload: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> ProdutoModel:
    _ = current_user
    produto = ProdutoModel(**payload.model_dump())
    try:
        db.add(produto)
        db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.PRODUTO,
            recurso_id=produto.id,
            dados_novos=_produto_to_dict(produto),
        )
        db.commit()
        db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {exc}")


@router.put("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_produto(
    request: Request,
    id: int,
    payload: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> ProdutoModel:
    _ = current_user
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
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

        db.commit()
        db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar produto: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_produto(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
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
        db.delete(produto)
        db.commit()
        return {"detail": "Produto removido com sucesso"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover produto: {exc}")