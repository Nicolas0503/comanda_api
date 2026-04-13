from sqlalchemy import Column, Integer

from infra.database import Base


class ComandaItemModel(Base):
    __tablename__ = "comanda_itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comanda_id = Column(Integer, nullable=False, index=True)
    produto_id = Column(Integer, nullable=False, index=True)
    quantidade = Column(Integer, nullable=False, default=1)
