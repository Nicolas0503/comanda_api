from sqlalchemy import Column, Integer, String

from infra.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    telefone = Column(String(20), nullable=True)
