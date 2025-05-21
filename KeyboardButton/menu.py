from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os
import configparser

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from weather.weather import get_weather

# 取得目前檔案所在的資料夾
current_dir = os.path.dirname(os.path.abspath(__file__))

# 找到 env.ini 的完整路徑
ini_path = os.path.join(current_dir, '..', 'env.ini')

# 建立 configparser 實例
config = configparser.ConfigParser()

# 讀取 env.ini
config.read(ini_path, encoding="utf-8")

BOT_Token = config['Key']['BOT_Token']

# 台灣簡易縣市資料
# 讀取 JSON 檔案
with open(os.path.join("files", "location.json"), "r", encoding="utf-8") as f:
    taiwan_data = json.load(f)

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(region, callback_data=f"region:{region}")]
        for region in taiwan_data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("請選擇區域：", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("region:"):
        region     = data.split(":", 1)[1]
        cities     = taiwan_data.get(region, {})
        keyboard   = [
            [InlineKeyboardButton(city, callback_data=f"city:{region}:{city}")]
            for city in cities.keys()
        ]
        keyboard.append([InlineKeyboardButton("返回區域選單", callback_data="back_to_region")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"請選擇 {region} 的縣市：", reply_markup=reply_markup)

    elif data.startswith("city:"):
        _, region, city = data.split(":", 2)
        districts = taiwan_data.get(region, {}).get(city, [])
        keyboard = [
            [InlineKeyboardButton(district, callback_data=f"district:{region}:{city}:{district}")]
            for district in districts
        ]
        keyboard.append([InlineKeyboardButton("返回縣市選單", callback_data=f"back_to_city:{region}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"請選擇 {city} 的鄉鎮區：", reply_markup=reply_markup)

    elif data.startswith("district:"):
        _, region, city, district = data.split(":", 3)
        # 呼叫 weather.py 查詢天氣
        weather_info = get_weather(city, district)
        await query.edit_message_text(
            f"你選擇的是：{region} - {city} - {district}\n\n🌤️ 24小時天氣預報\n{weather_info}"
        )
    elif data == "back_to_region":
        keyboard = [
            [InlineKeyboardButton(region, callback_data=f"region:{region}")]
            for region in taiwan_data.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("請選擇區域：", reply_markup=reply_markup)

    elif data.startswith("back_to_city:"):
        region = data.split(":", 1)[1]
        cities = taiwan_data.get(region, {})
        keyboard = [
            [InlineKeyboardButton(city, callback_data=f"city:{region}:{city}")]
            for city in cities.keys()
        ]
        keyboard.append([InlineKeyboardButton("返回區域選單", callback_data="back_to_region")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"請選擇 {region} 的縣市：", reply_markup=reply_markup)
