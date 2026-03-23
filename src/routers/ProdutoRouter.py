from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.schemas.ProdutoSchema import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from infra.database import get_db
from infra.orm.ProdutoModel import ProdutoModel

router = APIRouter(prefix="/produtos", tags=["Produto"])


@router.get("/", response_model=list[ProdutoResponse], status_code=status.HTTP_200_OK)
async def listar_produtos(db: Session = Depends(get_db)) -> list[ProdutoModel]:
    return db.query(ProdutoModel).all()


@router.get("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
async def buscar_produto_por_id(id: int, db: Session = Depends(get_db)) -> ProdutoModel:
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return produto


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)) -> ProdutoModel:
    produto = ProdutoModel(**payload.model_dump())
    try:
        db.add(produto)
        db.commit()
        db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {exc}")


@router.put("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
async def atualizar_produto(
    id: int, payload: ProdutoUpdate, db: Session = Depends(get_db)
) -> ProdutoModel:
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    dados = payload.model_dump(exclude_unset=True)
    try:
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        db.commit()
        db.refresh(produto)
        return produto
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar produto: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def remover_produto(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    try:
        db.delete(produto)
        db.commit()
        return {"detail": "Produto removido com sucesso"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover produto: {exc}")