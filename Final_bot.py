from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from translatepy import Translator
import pycountry

TOKEN = "7953125206:AAE99NQfaJrSLu7pWkLy-3EwoJtJUssTYr0"  # Replace this with your actual bot token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ HealixBot မှကြိုဆိုပါတယ်။")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ဘာသာပြန်ဖို့ /[ဘာသာကုဒ်] [စာသား] လို့ရိုက်ပါ။\n"
        "ဥပမာ:\n"
        "/my မင်္ဂလာပါ\n"
        "/en I love you\n"
        "/ja Good morning\n\n"
        "ISO 639-1 ဘာသာကုဒ် ၁၀၀ ကျော်ကို ထောက်ခံပါတယ်။"
    )


async def translate_dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split()[0][1:].lower()

    if not pycountry.languages.get(alpha_2=command):
        await update.message.reply_text(f"Invalid language code: {command}")
        return

    args = update.message.text.split()[1:]
    if not args:
        await update.message.reply_text(f"အသုံးပြုပုံ: /{command} [ဘာသာပြန်လိုသော စာသား]")
        return

    text_to_translate = ' '.join(args)

    try:
        translator = Translator()
        result = translator.translate(text_to_translate, destination_language=command)
        await update.message.reply_text(result.result)  # Only the translation
    except Exception as e:
        await update.message.reply_text(f"မှားယွင်းမှု: {str(e)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hello" in text:
        response = "Hello! I'm HealixBot!"
    elif "how are you" in text or "နေကောင်းလား" in text:
        response = "I'm great! How about you?"
    elif "who created you" in text or "ဘယ်သူဖန်တီးတာလဲ" in text:
        response = "My creator is Sayar_Zein!"
    elif "most beautiful person" in text:
        response = "Aye Chan Myae is the most beautiful!"
    else:
        response = "I'm not sure how to respond to that."

    await update.message.reply_text(response)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.COMMAND, translate_dynamic))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()