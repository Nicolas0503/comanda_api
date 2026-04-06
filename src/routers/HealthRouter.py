import os
import platform
from datetime import UTC, datetime

import psutil
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from infra.database import engine, get_db
from infra.rate_limit import limiter, limits
from settings import (
    HEALTH_FAIL_CPU_PERCENT,
    HEALTH_FAIL_DISK_PERCENT,
    HEALTH_FAIL_MEMORY_PERCENT,
    HEALTH_WARN_CPU_PERCENT,
    HEALTH_WARN_DISK_PERCENT,
    HEALTH_WARN_MEMORY_PERCENT,
)

router = APIRouter(tags=["Health"])

EXPECTED_TABLES = {
    "funcionarios",
    "clientes",
    "produtos",
    "auditoria",
}


def _classify(metric_value: float, warn: float, fail: float) -> str:
    if metric_value >= fail:
        return "unhealthy"
    if metric_value >= warn:
        return "warning"
    return "healthy"


def _database_status(db: Session) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "detail": "Conexao com banco valida"}
    except Exception as exc:
        return {"status": "unhealthy", "detail": f"Falha ao conectar no banco: {exc}"}


def _tables_status() -> dict:
    try:
        inspector = inspect(engine)
        existing = set(inspector.get_table_names())
        missing = sorted(EXPECTED_TABLES - existing)

        if missing:
            return {
                "status": "unhealthy",
                "detail": "Tabelas obrigatorias ausentes",
                "missing_tables": missing,
                "existing_tables": sorted(existing),
            }

        return {
            "status": "healthy",
            "detail": "Todas as tabelas obrigatorias estao disponiveis",
            "tables": sorted(existing),
        }
    except Exception as exc:
        return {"status": "unhealthy", "detail": f"Falha ao validar tabelas: {exc}"}


def _system_status() -> dict:
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage(os.getcwd()).percent

    cpu_status = _classify(cpu, HEALTH_WARN_CPU_PERCENT, HEALTH_FAIL_CPU_PERCENT)
    memory_status = _classify(memory, HEALTH_WARN_MEMORY_PERCENT, HEALTH_FAIL_MEMORY_PERCENT)
    disk_status = _classify(disk, HEALTH_WARN_DISK_PERCENT, HEALTH_FAIL_DISK_PERCENT)

    statuses = [cpu_status, memory_status, disk_status]
    if "unhealthy" in statuses:
        overall = "unhealthy"
    elif "warning" in statuses:
        overall = "warning"
    else:
        overall = "healthy"

    return {
        "status": overall,
        "metrics": {
            "cpu_percent": {"value": cpu, "status": cpu_status},
            "memory_percent": {"value": memory, "status": memory_status},
            "disk_percent": {"value": disk, "status": disk_status},
        },
        "system": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
        },
    }


@router.get("/health", status_code=status.HTTP_200_OK)
@limiter.limit(limits.low)
async def health_basic(request: Request):
    _ = request
    return {
        "status": "healthy",
        "service": "comandas_api",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/health/database", status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def health_database(request: Request, db: Session = Depends(get_db)):
    _ = request
    return _database_status(db)


@router.get("/health/database/tables", status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def health_database_tables(request: Request):
    _ = request
    return _tables_status()


@router.get("/health/system", status_code=status.HTTP_200_OK)
@limiter.limit(limits.low)
async def health_system(request: Request):
    _ = request
    return _system_status()


@router.get("/health/full", status_code=status.HTTP_200_OK)
@limiter.limit(limits.restrictive)
async def health_full(request: Request, db: Session = Depends(get_db)):
    _ = request
    db_info = _database_status(db)
    table_info = _tables_status()
    system_info = _system_status()

    statuses = [db_info["status"], table_info["status"], system_info["status"]]
    if "unhealthy" in statuses:
        overall = "unhealthy"
    elif "warning" in statuses:
        overall = "warning"
    else:
        overall = "healthy"

    return {
        "status": overall,
        "checks": {
            "database": db_info,
            "tables": table_info,
            "system": system_info,
        },
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
@limiter.limit(limits.moderate)
async def readiness(request: Request, db: Session = Depends(get_db)):
    _ = request
    db_info = _database_status(db)
    table_info = _tables_status()

    if db_info["status"] != "healthy" or table_info["status"] != "healthy":
        return {
            "status": "unhealthy",
            "checks": {
                "database": db_info,
                "tables": table_info,
            },
        }

    return {
        "status": "healthy",
        "checks": {
            "database": db_info,
            "tables": table_info,
        },
    }


@router.get("/live", status_code=status.HTTP_200_OK)
@limiter.limit(limits.low)
async def liveness(request: Request):
    _ = request
    return {
        "status": "healthy",
        "detail": "Aplicacao em execucao",
        "timestamp": datetime.now(UTC).isoformat(),
    }
