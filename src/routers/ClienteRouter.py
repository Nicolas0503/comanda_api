from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ClienteSchema import ClienteCreate, ClienteResponse, ClienteUpdate
from infra.database import get_db
from infra.orm.ClienteModel import ClienteModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user, require_group
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria

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
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> list[ClienteModel]:
    _ = request
    _ = current_user
    return db.query(ClienteModel).all()


@router.get("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_cliente_por_id(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> ClienteModel:
    _ = request
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_cliente(
    request: Request,
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
        db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.CLIENTE,
            recurso_id=cliente.id,
            dados_novos=_cliente_to_dict(cliente),
        )
        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {exc}")


@router.put("/{id}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_cliente(
    request: Request,
    id: int,
    payload: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
) -> ClienteModel:
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    dados_antigos = _cliente_to_dict(cliente)

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

        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cliente: {exc}")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_cliente(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
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
        db.delete(cliente)
        db.commit()
        return {"detail": "Cliente removido com sucesso"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover cliente: {exc}")