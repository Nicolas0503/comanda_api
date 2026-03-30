from pydantic import BaseModel, ConfigDict


class FuncionarioBase(BaseModel):
    nome: str
    matricula: str
    cpf: str
    telefone: str | None = None
    grupo: str
    senha: str


class FuncionarioCreate(FuncionarioBase):
    pass


class FuncionarioUpdate(BaseModel):
    nome: str | None = None
    matricula: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    grupo: str | None = None
    senha: str | None = None


class FuncionarioResponse(FuncionarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
