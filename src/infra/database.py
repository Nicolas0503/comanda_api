from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from settings import (
    BOOTSTRAP_ADMIN_CPF,
    BOOTSTRAP_ADMIN_GRUPO,
    BOOTSTRAP_ADMIN_MATRICULA,
    BOOTSTRAP_ADMIN_NOME,
    BOOTSTRAP_ADMIN_SENHA,
    BOOTSTRAP_ADMIN_TELEFONE,
    STR_DATABASE,
)


def _build_async_database_url() -> str:
    if STR_DATABASE.startswith("sqlite:///"):
        return STR_DATABASE.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    if "://" in STR_DATABASE and "+" not in STR_DATABASE.split("://", 1)[0]:
        return STR_DATABASE.replace("://", "+asyncpg://", 1)
    return STR_DATABASE


ASYNC_DATABASE_URL = _build_async_database_url()

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False} if ASYNC_DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()


async def cria_tabelas() -> None:
    from infra.orm.AuditoriaModel import AuditoriaModel
    from infra.orm.ClienteModel import ClienteModel
    from infra.orm.ComandaItemModel import ComandaItemModel
    from infra.orm.ComandaModel import ComandaModel
    from infra.orm.FuncionarioModel import FuncionarioModel
    from infra.orm.ProdutoModel import ProdutoModel

    _ = (
        ClienteModel,
        FuncionarioModel,
        ProdutoModel,
        AuditoriaModel,
        ComandaModel,
        ComandaItemModel,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def cria_admin_bootstrap_se_necessario() -> None:
    from infra.orm.FuncionarioModel import FuncionarioModel

    async with SessionLocal() as db:
        admin_existente = await db.scalar(
            select(FuncionarioModel).where(
                (FuncionarioModel.matricula == BOOTSTRAP_ADMIN_MATRICULA)
                | (FuncionarioModel.cpf == BOOTSTRAP_ADMIN_CPF)
            )
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
        await db.commit()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


# Backward-compatible alias for existing imports.
get_db = get_async_db
