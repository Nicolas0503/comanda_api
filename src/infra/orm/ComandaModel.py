from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from infra.database import Base


class ComandaModel(Base):
    __tablename__ = "comandas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(30), nullable=False, unique=True, index=True)
    status = Column(String(30), nullable=False, index=True, default="ABERTA")
    cliente_id = Column(Integer, nullable=False, index=True)
    funcionario_id = Column(Integer, nullable=False, index=True)
    data_abertura = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    data_fechamento = Column(DateTime, nullable=True)
