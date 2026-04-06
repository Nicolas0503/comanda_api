# Nicolas Bastos

from contextlib import asynccontextmanager
from datetime import UTC, datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from infra.database import cria_admin_bootstrap_se_necessario, cria_tabelas
from infra.rate_limit import limiter
from routers import (
    AuditoriaRouter,
    AuthRouter,
    ClienteRouter,
    FuncionarioRouter,
    HealthRouter,
    ProdutoRouter,
)
from settings import HOST, PORT, RELOAD

#nícolas bastos
@asynccontextmanager
async def lifespan(_: FastAPI):
    await cria_tabelas()
    await cria_admin_bootstrap_se_necessario()
    yield


app = FastAPI(title="API Pastelaria", lifespan=lifespan)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "code": 429,
            "message": "Limite de requisicoes excedido",
            "path": str(request.url.path),
            "detail": str(exc.detail),
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )

app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)
app.include_router(AuthRouter.router)
app.include_router(AuditoriaRouter.router)
app.include_router(HealthRouter.router)


@app.get("/", tags=["Root"], status_code=200)
async def root() -> dict[str, str]:
    return {
        "detail": "API Pastelaria",
        "Swagger UI": "http://127.0.0.1:8000/docs",
        "ReDoc": "http://127.0.0.1:8000/redoc",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD)