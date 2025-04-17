import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

import ImagemModels
from ImagemModels import ImagemRequest
from Pessoa import carregar_pessoas

# Caminho onde estão as imagens
IMAGE_DIR = "./documentos"
OUTPUT_DIR = "./imagens/output"

# Cria pasta de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)


class CriarImagem:
    def __init__(self, request: ImagemRequest):
        print("Criando imagem")
        self.request = request
        self.pessoas = carregar_pessoas()

    def __call__(self, *args, **kwargs):
        print("Criando imagem em disco")
        pessoa = None
        for p in self.pessoas:
            if p.get("indice") == self.request.nome_pessoa:
                pessoa = p
                break
        nome_pessoa = pessoa["nome"]
        documentos = pessoa["documentos"]

        pais = [pessoa for pessoa in self.pessoas if pessoa.get("is_parent") == self.request.nome_responsavel]
        for p in pais:
            for d in p["documentos"]:
                documentos.append(d)

        documentos_com_marca_dagua = []
        for doc in documentos:
            caminho_entrada = os.path.join(IMAGE_DIR, doc)

            if not os.path.exists(caminho_entrada):
                raise CriarImagemException()

            with Image.open(caminho_entrada).convert("RGBA") as base:
                canvas = Image.new("RGBA", base.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(canvas)
                fonte = ImageFont.truetype("OldNewspaperTypes.ttf", 32)
                texto = self.request.local + " " + datetime.now().strftime("%d/%m/%Y %H:%M")
                text_w = int(draw.textlength(texto, font=fonte))
                text_h = 32
                espaco_x = text_w + 50
                espaco_y = text_h + 40

                largura, altura = base.size
                for y in range(0, altura, espaco_y):
                    for x in range(0, largura, espaco_x):
                        draw.text((x, y), texto, fill=(255, 0, 0, 20), font=fonte)
                out = Image.alpha_composite(base, canvas)
                now = datetime.now().strftime("%Y%m%d")
                caminho_saida = os.path.join(OUTPUT_DIR, doc.replace(".jpg", now + ".png"))
                out.save(caminho_saida)
                documentos_com_marca_dagua.append(caminho_saida)
        print("imagens", documentos_com_marca_dagua)
        return ImagemModels.ImagemGeradas(destinatario=self.request.destinatario,
                                          caminho_imagem=documentos_com_marca_dagua, pessoa=nome_pessoa)


class CriarImagemException(BaseException):
    __notes__ = "Erro ao criar imagem."

    def __str__(self):
        return self.__notes__

    pass
