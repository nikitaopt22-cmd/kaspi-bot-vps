import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from layout import build_a4_layout
from kaspi_api import KaspiAPI

DATA_DIR = "/home/youruser/kaspi_bot/data"
os.makedirs(DATA_DIR, exist_ok=True)

SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")
if not os.path.exists(SESSIONS_FILE):
    with open(SESSIONS_FILE, "w") as f:
        json.dump({}, f)

def _load_sessions():
    with open(SESSIONS_FILE, "r") as f:
        return json.load(f)

def _save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Загружайте накладные (PDF/ZIP). Я объединю их по заданной раскладке на A4."
    )

def set_layout(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    layout = int(context.args[0]) if context.args else 4
    if layout not in (4, 8, 9):
        update.message.reply_text("Допустимы раскладки: 4, 8, 9.")
        return
    sessions = _load_sessions()
    s = sessions.get(chat_id, {})
    s["layout"] = layout
    sessions[chat_id] = s
    _save_sessions(sessions)
    update.message.reply_text(f"Раскладка на A4 установлена: {layout} накладных на страницу.")

def set_pagesize(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    width = int(context.args[0]) if context.args else 75
    if width not in (75, 120, 100, 150):
        update.message.reply_text("Допустимые ширины: 75, 120, 100, 150.")
        return
    sessions = _load_sessions()
    s = sessions.get(chat_id, {})
    s["page_width"] = width
    sessions[chat_id] = s
    _save_sessions(sessions)
    update.message.reply_text(f"Ширина печати установлена: {width} мм.")

def _extract_pdf_paths_from_message(update: Update, context: CallbackContext):
    msg = update.message
    user_id = str(msg.from_user.id)
    pdf_paths = []
    if msg.document:
        for doc in msg.document:
            file = context.bot.get_file(doc.file_id)
            data = file.download_as_bytearray()
            fname = doc.file_name or "attachment"
            path = os.path.join(DATA_DIR, f"{user_id}_{fname}")
            with open(path, "wb") as f:
                f.write(data)
            if fname.lower().endswith(".pdf"):
                pdf_paths.append(path)
            elif fname.lower().endswith(".zip"):
                import zipfile
                zf = zipfile.ZipFile(path)
                for name in zf.namelist():
                    if name.lower().endswith(".pdf"):
                        outp = os.path.join(DATA_DIR, f"{user_id}_{name}")
                        with zf.open(name) as src, open(outp, "wb") as dst:
                            dst.write(src.read())
                        pdf_paths.append(outp)
    return pdf_paths

def print_merged(update: Update, context: CallbackContext):
    msg = update.message
    chat_id = str(msg.chat.id)
    pdf_paths = _extract_pdf_paths_from_message(update, context)
    if not pdf_paths:
        update.message.reply_text("Не найдено PDF/Nach накладных в загрузках.")
        return

    sessions = _load_sessions()
    s = sessions.get(chat_id, {})
    per_page = s.get("layout", 4)
    page_width = s.get("page_width", 75)

    out_pdf = os.path.join(DATA_DIR, f"{chat_id}_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    build_a4_layout(pdf_paths, out_pdf, per_page=per_page, page_width_mm=page_width)

    with open(out_pdf, "rb") as f:
        msg.reply_document(document=f, filename=os.path.basename(out_pdf),
                           caption=f"Объединённый PDF ({per_page} на страницу, {page_width} мм).")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_layout", set_layout, pass_args=True))
    dp.add_handler(CommandHandler("set_pagesize", set_pagesize, pass_args=True))
    dp.add_handler(MessageHandler(Filters.document, print_merged))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
