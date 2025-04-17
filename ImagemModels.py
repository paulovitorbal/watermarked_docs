from typing import List, Any

from pydantic import BaseModel


class ImagemRequest(BaseModel):
    nome_pessoa: str
    local: str
    destinatario: str
    nome_responsavel: str

class ImagemGeradas(BaseModel):
    destinatario: str
    caminho_imagem: List[str]
    pessoa: str