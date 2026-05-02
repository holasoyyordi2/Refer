from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

TOKEN = "8799995408:AAEoSUzt_5Y8BqjW9Jg9OtppVGCdIdk1d1Q"
FORO_ID = -1003915971786

pinned_message_id = None
user_activity = defaultdict(datetime.now)   # Guarda última actividad

# ================== REFERENCIAS ==================
async def referencias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❌ Responde a una imagen con /referencias o .referencias")
        return
    photo = update.message.reply_to_message.photo[-1]
    await context.bot.send_photo(FORO_ID, photo.file_id, caption="🚀 Nueva Referencia ⛩️ Team Umbrella")
    await update.message.reply_text("✅ Referencia enviada 🔥")

# ================== INACTIVES (funciona) ==================
async def inactives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = 7
    if context.args:
        try:
            days = int(context.args[0])
        except:
            pass
    
    cutoff = datetime.now() - timedelta(days=days)
    inactive = [user for user, last in user_activity.items() if last < cutoff]
    
    if inactive:
        text = f"🔴 Usuarios inactivos más de {days} días:\n"
        for user in inactive[:20]:  # máximo 20
            text += f"• {user}\n"
        await update.message.reply_text(text[:4000])
    else:
        await update.message.reply_text("✅ No hay usuarios inactivos.")

# ================== Resto de comandos ==================
async def geturl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Responde a un mensaje.")
        return
    msg = update.message.reply_to_message
    if msg.chat.username:
        url = f"https://t.me/{msg.chat.username}/{msg.message_id}"
        await update.message.reply_text(f"🔗 Enlace:\n{url}")
    else:
        await update.message.reply_text("❌ Grupo necesita @username.")

async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pinned_message_id
    if update.message.reply_to_message:
        m = await context.bot.forward_message(FORO_ID, update.message.chat.id, update.message.reply_to_message.message_id)
        await context.bot.pin_chat_message(FORO_ID, m.message_id)
        pinned_message_id = m.message_id
        await update.message.reply_text("📌 Mensaje fijado.")
    else:
        await update.message.reply_text("❌ Responde a un mensaje.")

async def delpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pinned_message_id
    if pinned_message_id:
        await context.bot.unpin_chat_message(FORO_ID)
        pinned_message_id = None
        await update.message.reply_text("🗑️ Fijado eliminado.")
    else:
        await update.message.reply_text("❌ No hay mensaje fijado.")

# Actualizar actividad
async def track_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_activity[update.effective_user.id] = datetime.now()

# ================== MAIN ==================
def main():
    app = Application.builder().token(TOKEN).build()

    # Referencias
    app.add_handler(CommandHandler("referencias", referencias))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^\.referencias'), referencias))

    # Track activity
    app.add_handler(MessageHandler(filters.ALL, track_activity), group=1)

    # Comandos
    app.add_handler(CommandHandler("geturl", geturl))
    app.add_handler(CommandHandler("pin", pin))
    app.add_handler(CommandHandler("delpin", delpin))
    app.add_handler(CommandHandler("inactives", inactives))

    print("🚀 Team Umbrella Bot - Versión Avanzada")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
