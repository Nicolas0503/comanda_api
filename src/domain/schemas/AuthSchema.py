from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    login: str
    senha: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class FuncionarioAuth(BaseModel):
    id: int
    nome: str
    matricula: str
    cpf: str
    telefone: str | None = None
    grupo: str

    model_config = ConfigDict(from_attributes=True)
