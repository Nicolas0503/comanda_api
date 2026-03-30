from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from infra.database import cria_admin_bootstrap_se_necessario, cria_tabelas
from routers import AuthRouter, ClienteRouter, FuncionarioRouter, ProdutoRouter
from settings import HOST, PORT, RELOAD

#nícolas bastos
@asynccontextmanager
async def lifespan(_: FastAPI):
    await cria_tabelas()
    await cria_admin_bootstrap_se_necessario()
    yield


app = FastAPI(title="API Pastelaria", lifespan=lifespan)

app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)
app.include_router(AuthRouter.router)


@app.get("/", tags=["Root"], status_code=200)
async def root() -> dict[str, str]:
    return {
        "detail": "API Pastelaria",
        "Swagger UI": "http://127.0.0.1:8000/docs",
        "ReDoc": "http://127.0.0.1:8000/redoc",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD)