from pydantic import BaseModel, ConfigDict


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    foto: bytes | None = None
    valor_unitario: float


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    foto: bytes | None = None
    valor_unitario: float | None = None


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
