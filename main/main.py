from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler
import os
import configparser

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from KeyboardButton.menu import select, button_handler


# 取得目前檔案所在的資料夾
current_dir = os.path.dirname(os.path.abspath(__file__))

# 找到 env.ini 的完整路徑
ini_path = os.path.join(current_dir, '..', 'env.ini')

# 建立 configparser 實例
config = configparser.ConfigParser()

# 讀取 env.ini
config.read(ini_path, encoding="utf-8")

BOT_Token = config['Key']['BOT_Token']

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("感謝使用")
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await select(update, context)    
    
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_Token).build()
    
    app.add_handler(CommandHandler("start", welcome))
    app.add_handler(CommandHandler("weather", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()
