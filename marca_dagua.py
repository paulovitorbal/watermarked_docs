from CriarImagem import CriarImagem
from ImagemModels import ImagemRequest
from enviar_email import enviar_email

async def marca_dagua(req: ImagemRequest):
    print("Criando marca d'água")
    imagens = CriarImagem(req)
    resultado = imagens()
    enviar_email(resultado)