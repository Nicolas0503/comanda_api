from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditoriaResponse(BaseModel):
    id: int
    funcionario_id: int | None = None
    acao: str
    recurso: str
    recurso_id: int | None = None
    dados_antigos: str | None = None
    dados_novos: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    data_hora: datetime

    model_config = ConfigDict(from_attributes=True)
