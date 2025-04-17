import json
from typing import List, Any


class CarregarPessoaException(BaseException):
    __notes__ = "Erro ao carregar o arquivo pessoas.json."

    def __str__(self):
        return self.__notes__

    pass


def carregar_pessoas() -> List[dict[str, Any]]:
    with open("pessoas.json", "r") as file:
        pessoas = json.load(file)
    if not pessoas:
        raise CarregarPessoaException()
    return pessoas
