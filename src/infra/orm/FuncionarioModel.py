from sqlalchemy import Column, Integer, String

from infra.database import Base


class FuncionarioModel(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    matricula = Column(String(50), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    telefone = Column(String(20), nullable=True)
    grupo = Column(String(50), nullable=False)
    senha = Column(String(255), nullable=False)
