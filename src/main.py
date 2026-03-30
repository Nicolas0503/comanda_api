from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

#Nícolas Bastos

from routers import FuncionarioRouter
from routers import ClienteRouter
from routers import ProdutoRouter
from routers import AuthRouter

app = FastAPI()

app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)
app.include_router(AuthRouter.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=RELOAD)

# rota padrão (pública)
@app.get("/", tags=["Root"], status_code=200)
def root():
    return {"detail":"API Pastelaria", "Swagger UI": "http://127.0.0.1:8000/docs", "ReDoc": "http://127.0.0.1:8000/redoc" }