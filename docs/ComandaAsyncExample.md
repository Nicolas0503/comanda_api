# Exemplo de ComandaRouter Assincrono (GET com filtros + paginacao)

```python
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ComandaSchema import ComandaResponse
from infra.database import get_db
from infra.orm.ComandaModel import ComandaModel
from infra.rate_limit import limiter, limits
from security.auth import get_current_active_user
from services.QueryFilterService import (
    append_datetime_interval_filter,
    append_equal_filter,
    apply_filters,
    apply_pagination,
)

router = APIRouter(prefix="/comandas", tags=["Comanda"])


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
```

## Exemplo de chamada

`GET /comandas/?skip=0&limit=20&status=ABERTA&cliente_id=10&data_inicio=2026-01-01T00:00:00&data_fim=2026-12-31T23:59:59`
