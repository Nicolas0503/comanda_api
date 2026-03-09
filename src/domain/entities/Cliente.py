from pydantic import BaseModel

#Nícolas Bastos

class Cliente(BaseModel):
    id_cliente: int = None
    nome: str
    cpf: str
    telefone: str