import os
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import logging
from ollama import chat


load_dotenv()


BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user = update.effective_user
    
    await update.message.reply_html(generate(f"Greet the user '{user.first_name}'. Make sure to use users nickname ('{user.first_name}'). Introduce yourself as Llama2 ai assistant and in short explain what you are capable off"))
    global messages
    messages = [
    {'role': 'user', 'content': " "},
    ]



async def hist_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #/hist
    for x in messages:
        output = f"{x['role']}:\n{x['content']}\n"
        print(output)
        await update.message.reply_text(output)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #/clear
    global messages
    messages = [
    {'role': 'user', 'content': " "},
    ]
    await update.message.reply_text("Chat history cleared")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Generating...")
    await update.message.reply_text(generate(update.message.text))

messages = [
  {'role': 'user', 'content': " "},
]

def generate(prompt):
    global messages
    messages.append({'role': 'user', 'content': prompt})

    response = chat('llama2-uncensored', messages=messages)
    message = response['message']
    print("Prompt:\n" + prompt)
    print("Response:\n" + str(message['content']))
    #print(messages)
    messages.append(message)
    if (message == ''):
        return "Error"
    else:
        return message['content']

def main() -> None:
    """Start the bot."""

    application = Application.builder().token(BOT_TOKEN).build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("hist", hist_command))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()