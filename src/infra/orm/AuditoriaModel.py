from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from infra.database import Base


class AuditoriaModel(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_id = Column(Integer, nullable=True, index=True)
    acao = Column(String(20), nullable=False, index=True)
    recurso = Column(String(30), nullable=False, index=True)
    recurso_id = Column(Integer, nullable=True)
    dados_antigos = Column(Text, nullable=True)
    dados_novos = Column(Text, nullable=True)
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
