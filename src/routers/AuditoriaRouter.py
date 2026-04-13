from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuditoriaSchema import AuditoriaResponse
from domain.schemas.AuthSchema import FuncionarioAuth
from infra.database import get_db
from infra.orm.AuditoriaModel import AuditoriaModel
from infra.rate_limit import limiter, limits
from security.auth import require_group
from services.QueryFilterService import (
    append_datetime_interval_filter,
    append_equal_filter,
    append_ilike_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])


@router.get("/", response_model=list[AuditoriaResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_auditoria(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    id: int | None = Query(None),
    funcionario: int | None = Query(None, alias="funcionario"),
    acao: str | None = Query(None),
    recurso: str | None = Query(None),
    ip: str | None = Query(None),
    data: datetime | None = Query(None),
    data_inicio: datetime | None = Query(None),
    data_fim: datetime | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> list[AuditoriaModel]:
    _ = request
    _ = current_user

    if data is not None and (data_inicio is not None or data_fim is not None):
        raise HTTPException(
            status_code=400,
            detail="Use data exata ou data_inicio/data_fim, nao ambos",
        )

    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(status_code=400, detail="data_inicio nao pode ser maior que data_fim")

    filters: list = []
    append_equal_filter(filters, AuditoriaModel.id, id)
    append_equal_filter(filters, AuditoriaModel.funcionario_id, funcionario)
    append_equal_filter(filters, AuditoriaModel.acao, acao)
    append_equal_filter(filters, AuditoriaModel.recurso, recurso)
    append_ilike_filter(filters, AuditoriaModel.ip_address, ip)

    if data is not None:
        append_datetime_interval_filter(
            filters,
            AuditoriaModel.data_hora,
            start_at=data,
            end_at=data,
        )
    else:
        append_datetime_interval_filter(
            filters,
            AuditoriaModel.data_hora,
            start_at=data_inicio,
            end_at=data_fim,
        )

    statement = select(AuditoriaModel).order_by(AuditoriaModel.data_hora.desc())
    statement = apply_filters(statement, filters)
    statement = apply_pagination(statement, skip=skip, limit=limit)

    result = await db.scalars(statement)
    return result.all()
