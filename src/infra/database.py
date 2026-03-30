import asyncio
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import (
    BOOTSTRAP_ADMIN_CPF,
    BOOTSTRAP_ADMIN_GRUPO,
    BOOTSTRAP_ADMIN_MATRICULA,
    BOOTSTRAP_ADMIN_NOME,
    BOOTSTRAP_ADMIN_SENHA,
    BOOTSTRAP_ADMIN_TELEFONE,
    STR_DATABASE,
)


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


async def cria_admin_bootstrap_se_necessario() -> None:
    from infra.orm.FuncionarioModel import FuncionarioModel

    def _run() -> None:
        db = SessionLocal()
        try:
            admin_existente = (
                db.query(FuncionarioModel)
                .filter(
                    (FuncionarioModel.matricula == BOOTSTRAP_ADMIN_MATRICULA)
                    | (FuncionarioModel.cpf == BOOTSTRAP_ADMIN_CPF)
                )
                .first()
            )
            if admin_existente:
                return

            admin = FuncionarioModel(
                nome=BOOTSTRAP_ADMIN_NOME,
                matricula=BOOTSTRAP_ADMIN_MATRICULA,
                cpf=BOOTSTRAP_ADMIN_CPF,
                telefone=BOOTSTRAP_ADMIN_TELEFONE,
                grupo=str(BOOTSTRAP_ADMIN_GRUPO),
                senha=BOOTSTRAP_ADMIN_SENHA,
            )
            db.add(admin)
            db.commit()
        finally:
            db.close()

    await asyncio.to_thread(_run)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
