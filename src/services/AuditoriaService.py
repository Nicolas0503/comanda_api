import json
from datetime import UTC, datetime
from enum import StrEnum

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from infra.orm.AuditoriaModel import AuditoriaModel


class AcaoAuditoria(StrEnum):
    LOGIN = "LOGIN"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class RecursoAuditoria(StrEnum):
    FUNCIONARIO = "FUNCIONARIO"
    CLIENTE = "CLIENTE"
    PRODUTO = "PRODUTO"
    COMANDA = "COMANDA"
    COMANDA_ITEM = "COMANDA_ITEM"
    AUTH = "AUTH"


class AuditoriaService:
    @staticmethod
    def _to_json(data: dict | None) -> str | None:
        if data is None:
            return None
        return json.dumps(data, ensure_ascii=True, default=str)

    @staticmethod
    def registrar(
        db: AsyncSession,
        request: Request,
        funcionario_id: int | None,
        acao: AcaoAuditoria,
        recurso: RecursoAuditoria,
        recurso_id: int | None = None,
        dados_antigos: dict | None = None,
        dados_novos: dict | None = None,
    ) -> AuditoriaModel:
        ip_address = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        if not ip_address and request.client:
            ip_address = request.client.host

        evento = AuditoriaModel(
            funcionario_id=funcionario_id,
            acao=acao.value,
            recurso=recurso.value,
            recurso_id=recurso_id,
            dados_antigos=AuditoriaService._to_json(dados_antigos),
            dados_novos=AuditoriaService._to_json(dados_novos),
            ip_address=ip_address or "unknown",
            user_agent=request.headers.get("user-agent"),
            data_hora=datetime.now(UTC).replace(tzinfo=None),
        )

        db.add(evento)
        return evento
