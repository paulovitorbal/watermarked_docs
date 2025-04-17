import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import ImagemModels


def enviar_email(imagens: ImagemModels.ImagemGeradas):
    load_dotenv()
    print("enviando e-mail")
    destinatario, caminho_imagem, pessoa = imagens.destinatario, imagens.caminho_imagem, imagens.pessoa
    # Configurações do remetente
    remetente = os.getenv("EMAIL_SENDER")
    senha = os.getenv("EMAIL_PASSWORD")

    # Criação do e-mail
    msg = EmailMessage()
    msg["Subject"] = "Documentos - "+pessoa
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content("Seguem os documentos solicitados.")

    for caminho in caminho_imagem:
        # Lê a imagem e adiciona como anexo
        with open(caminho, "rb") as img:
            nome_arquivo = os.path.basename(caminho)
            msg.add_attachment(img.read(), maintype="image", subtype="png", filename=nome_arquivo)

    # Envia o e-mail via SMTP do Gmail
    with smtplib.SMTP_SSL(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)
    print("E-mail enviado com sucesso!")
    pass