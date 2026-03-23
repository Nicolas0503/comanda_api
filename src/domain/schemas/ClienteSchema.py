from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    nome: str
    cpf: str
    telefone: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None


class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
