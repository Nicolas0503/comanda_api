from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.FuncionarioSchema import (
    FuncionarioCreate,
    FuncionarioResponse,
    FuncionarioUpdate,
)
from domain.schemas.AuthSchema import FuncionarioAuth
from infra.database import get_db
from infra.orm.FuncionarioModel import FuncionarioModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user, require_group
from services.AuditoriaService import AcaoAuditoria, AuditoriaService, RecursoAuditoria
from services.QueryFilterService import (
    append_equal_filter,
    append_ilike_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/funcionarios", tags=["Funcionario"])


def _funcionario_to_dict(funcionario: FuncionarioModel) -> dict:
    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "matricula": funcionario.matricula,
        "cpf": funcionario.cpf,
        "telefone": funcionario.telefone,
        "grupo": funcionario.grupo,
    }


@router.get("/", response_model=list[FuncionarioResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_funcionarios(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    id: int | None = Query(None),
    nome: str | None = Query(None),
    matricula: str | None = Query(None),
    cpf: str | None = Query(None),
    grupo: str | None = Query(None),
    telefone: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> list[FuncionarioModel]:
    _ = request
    _ = current_user

    filters: list = []
    append_equal_filter(filters, FuncionarioModel.id, id)
    append_ilike_filter(filters, FuncionarioModel.nome, nome)
    append_equal_filter(filters, FuncionarioModel.matricula, matricula)
    append_equal_filter(filters, FuncionarioModel.cpf, cpf)
    append_equal_filter(filters, FuncionarioModel.grupo, grupo)
    append_equal_filter(filters, FuncionarioModel.telefone, telefone)

    statement = select(FuncionarioModel).order_by(FuncionarioModel.id)
    statement = apply_filters(statement, filters)
    statement = apply_pagination(statement, skip=skip, limit=limit)

    result = await db.scalars(statement)
    return result.all()


@router.get("/{id}", response_model=FuncionarioResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def buscar_funcionario_por_id(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
) -> FuncionarioModel:
    _ = request
    _ = current_user
    funcionario = await db.scalar(select(FuncionarioModel).where(FuncionarioModel.id == id))
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")
    return funcionario


@router.post("/", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(limits.restrictive)
async def criar_funcionario(
    request: Request,
    payload: FuncionarioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> FuncionarioModel:
    _ = current_user
    if await db.scalar(select(FuncionarioModel).where(FuncionarioModel.cpf == payload.cpf)):
        raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    funcionario = FuncionarioModel(**payload.model_dump())
    try:
        db.add(funcionario)
        await db.flush()
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.CREATE,
            recurso=RecursoAuditoria.FUNCIONARIO,
            recurso_id=funcionario.id,
            dados_novos=_funcionario_to_dict(funcionario),
        )
        await db.commit()
        await db.refresh(funcionario)
        return funcionario
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar funcionario: {exc}")


@router.put("/{id}", response_model=FuncionarioResponse, status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def atualizar_funcionario(
    request: Request,
    id: int,
    payload: FuncionarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> FuncionarioModel:
    _ = current_user
    funcionario = await db.scalar(select(FuncionarioModel).where(FuncionarioModel.id == id))
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")

    dados_antigos = _funcionario_to_dict(funcionario)

    dados = payload.model_dump(exclude_unset=True)
    if "cpf" in dados:
        cpf_existente = (
            await db.scalar(
                select(FuncionarioModel).where(
                    FuncionarioModel.cpf == dados["cpf"],
                    FuncionarioModel.id != id,
                )
            )
        )
        if cpf_existente:
            raise HTTPException(status_code=409, detail="CPF ja cadastrado")

    try:
        for campo, valor in dados.items():
            setattr(funcionario, campo, valor)

        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.UPDATE,
            recurso=RecursoAuditoria.FUNCIONARIO,
            recurso_id=funcionario.id,
            dados_antigos=dados_antigos,
            dados_novos=_funcionario_to_dict(funcionario),
        )

        await db.commit()
        await db.refresh(funcionario)
        return funcionario
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar funcionario: {exc}",
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def remover_funcionario(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> dict[str, str]:
    _ = current_user
    funcionario = await db.scalar(select(FuncionarioModel).where(FuncionarioModel.id == id))
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario nao encontrado")

    dados_antigos = _funcionario_to_dict(funcionario)

    try:
        AuditoriaService.registrar(
            db=db,
            request=request,
            funcionario_id=current_user.id,
            acao=AcaoAuditoria.DELETE,
            recurso=RecursoAuditoria.FUNCIONARIO,
            recurso_id=funcionario.id,
            dados_antigos=dados_antigos,
        )
        await db.delete(funcionario)
        await db.commit()
        return {"detail": "Funcionario removido com sucesso"}
    except SQLAlchemyError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover funcionario: {exc}")