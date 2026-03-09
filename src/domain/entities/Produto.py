from pydantic import BaseModel

#Nícolas Bastos 

class Produto(BaseModel):    
    id_produto: int = None
    nome: str
    descricao: str 
    foto: str = None
    valor_unitario: float = None