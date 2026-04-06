from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from domain.schemas.AuditoriaSchema import AuditoriaResponse
from domain.schemas.AuthSchema import FuncionarioAuth
from infra.database import get_db
from infra.orm.AuditoriaModel import AuditoriaModel
from infra.rate_limit import limiter, limits
from security.auth import require_group

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])


@router.get("/", response_model=list[AuditoriaResponse], status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def listar_auditoria(
    request: Request,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
) -> list[AuditoriaModel]:
    _ = request
    _ = current_user
    return db.query(AuditoriaModel).order_by(AuditoriaModel.data_hora.desc()).limit(limit).all()
