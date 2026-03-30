from sqlalchemy import Column, Float, Integer, LargeBinary, String

from infra.database import Base


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    foto = Column(LargeBinary, nullable=True)
    valor_unitario = Column(Float, nullable=False)
