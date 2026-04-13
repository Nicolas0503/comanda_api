from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ComandaBase(BaseModel):
    numero: str
    status: str = "ABERTA"
    cliente_id: int
    funcionario_id: int
    data_abertura: datetime | None = None
    data_fechamento: datetime | None = None


class ComandaCreate(ComandaBase):
    pass


class ComandaUpdate(BaseModel):
    numero: str | None = None
    status: str | None = None
    cliente_id: int | None = None
    funcionario_id: int | None = None
    data_abertura: datetime | None = None
    data_fechamento: datetime | None = None


class ComandaResponse(ComandaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ComandaItemCreate(BaseModel):
    produto_id: int
    quantidade: int


class ComandaItemUpdate(BaseModel):
    quantidade: int


class ComandaItemResponse(BaseModel):
    item_id: int
    produto_id: int
    produto_nome: str
    produto_descricao: str
    quantidade: int


class ComandaProdutosResponse(BaseModel):
    comanda_id: int
    comanda_numero: str
    itens: list[ComandaItemResponse]
