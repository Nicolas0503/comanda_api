import asyncio
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import STR_DATABASE


engine = create_engine(
    STR_DATABASE,
    connect_args={"check_same_thread": False} if STR_DATABASE.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


async def cria_tabelas() -> None:
    from infra.orm.ClienteModel import ClienteModel
    from infra.orm.FuncionarioModel import FuncionarioModel
    from infra.orm.ProdutoModel import ProdutoModel

    _ = (ClienteModel, FuncionarioModel, ProdutoModel)
    await asyncio.to_thread(Base.metadata.create_all, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
