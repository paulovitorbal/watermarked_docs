import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, )
import marca_dagua
from ImagemModels import ImagemRequest
from Pessoa import carregar_pessoas

# Define states for the conversation
PERSON, RELATIONSHIP, EMAIL, LOCAL = range(4)
load_dotenv()

# Define the list of people (you can modify this as needed)
PEOPLE = [pessoa.get("indice") for pessoa in carregar_pessoas() if pessoa.get("is_parent") is not True]
PARENTS = [pessoa.get("indice") for pessoa in carregar_pessoas() if pessoa.get("is_parent")]
PARENTS.append("Nenhum")
PARENTS.append("Cancelar")
# Keyboard markup for people list and relationship options
PEOPLE_KEYBOARD = [[person] for person in PEOPLE]
PEOPLE_KEYBOARD.append(["Cancelar"])
RELATION_KEYBOARD = [[person] for person in PARENTS]
users = os.getenv("PERMITED_USERS")
if users:
    ALLOWED_USERS = users.split(",")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message to ask which person's info will be sent."""
    print(update.message.from_user)
    if users:
        if str(update.message.from_user.id) not in ALLOWED_USERS:
            await update.message.reply_text("Usuário não autorizado.", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
    reply_markup = ReplyKeyboardMarkup(PEOPLE_KEYBOARD, one_time_keyboard=True)
    await update.message.reply_text("Escolha a pessoa:", reply_markup=reply_markup)
    # Move to the next state
    return PERSON


async def ask_relationship(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask if they want to send father/mother info or none."""
    if update.message.text == "Cancelar":
        await update.message.reply_text("A conversa foi cancelada.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    # Save the selected person in the context
    context.user_data["person"] = update.message.text

    reply_markup = ReplyKeyboardMarkup(RELATION_KEYBOARD, one_time_keyboard=True)
    await update.message.reply_text(f"Você escolheu: {context.user_data['person']}. "
                                    "Agora, você deseja enviar também os documentos do pai, da mãe ou de nenhum?",
                                    reply_markup=reply_markup, )
    return RELATIONSHIP


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for the email address to send the information."""
    if update.message.text == "Cancelar":
        await update.message.reply_text("A conversa foi cancelada.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    # Save the selected relationship in context
    context.user_data["relationship"] = update.message.text

    await update.message.reply_text("Entendido, agora por favor informe o destinatário da mensagem (e-mail):",
                                    reply_markup=ReplyKeyboardRemove(), )
    return EMAIL


async def ask_local(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask for the email address to send the information."""
    if update.message.text == "Cancelar":
        await update.message.reply_text("A conversa foi cancelada.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    # Save the selected relationship in context
    context.user_data["email"] = update.message.text.strip()

    await update.message.reply_text("Entendido, agora por favor informe o local:", reply_markup=ReplyKeyboardRemove(), )
    return LOCAL


async def finish_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Finish the conversation and confirm the details."""
    # Save the email in context
    context.user_data["local"] = update.message.text.strip()

    # Determine what to send based on previous inputs
    person = context.user_data.get("person")
    relationship = context.user_data.get("relationship")
    email = context.user_data.get("email")
    local = context.user_data.get("local")

    summary = (f"- Pessoa: {person}\n"
               f"- Adicionar documentos dos pais: {relationship}\n"
               f"- Email do destinatário: {email}\n"
               f"- Local: {local}\n")
    await update.message.reply_text(
        f"Obrigado! Aqui estão os valores informados:\n{summary}O e-mail será enviado em breve.")
    await marca_dagua.marca_dagua(
        ImagemRequest(nome_pessoa=person, local=local, destinatario=email, nome_responsavel=relationship))
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    await update.message.reply_text("A conversa foi cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application with your bot's token
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Define the ConversationHandler for the flow
    conv_handler = ConversationHandler(entry_points=[CommandHandler("fotos", start)], states={
        PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_relationship)],
        RELATIONSHIP: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_local)],
        LOCAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_conversation)], },
                                       fallbacks=[CommandHandler("cancel", cancel)], )

    # Add the ConversationHandler to the application
    application.add_handler(conv_handler)

    # Run the bot until manually stopped
    application.run_polling()


if __name__ == "__main__":
    main()
