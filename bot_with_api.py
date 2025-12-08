import os
import asyncio
import re
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

# === Flask API для веб‑приложения ===

app_flask = Flask(__name__)
CORS(app_flask)  # Разрешаем CORS для запросов из Telegram Mini App

# Хранилище для мониторингов пользователей (по chat_id)
monitors: dict[int, dict] = {}


# === API Endpoints ===

@app_flask.route("/api/health", methods=["GET"])
def health_check():
    """Проверка работоспособности API"""
    return jsonify(
        {
            "status": "ok",
            "message": "Ozon Price API is running",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app_flask.route("/api/price", methods=["POST"])
def get_price_api():
    """
    API endpoint для получения цены товара
    POST /api/price
    Body: {"url": "https://www.ozon.ru/product/..."}
    """
    try:
        data = request.get_json() or {}
        url = data.get("url")

        if not url:
            return jsonify({"error": "URL не указан"}), 400

        if "ozon.ru" not in url.lower():
            return jsonify({"error": "Неверный URL (ожидается ссылка на Ozon)"}), 400

        price = get_price(url)

        if price is None:
            return jsonify({"error": "Не удалось получить цену", "url": url}), 404

        return jsonify(
            {
                "success": True,
                "price": price,
                "url": url,
                "currency": "RUB",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_flask.route("/api/monitors", methods=["GET"])
def get_monitors():
    """
    Получить список мониторингов пользователя
    GET /api/monitors?user_id=12345
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id не указан"}), 400

    try:
        chat_id = int(user_id)
    except ValueError:
        return jsonify({"error": "user_id должен быть числом"}), 400

    user_monitor = monitors.get(chat_id)

    return jsonify(
        {
            "success": True,
            "monitors": user_monitor or {},
            "count": 1 if user_monitor else 0,
        }
    )


# === Функция парсинга цены с Ozon ===

def get_price(url: str) -> int | None:
    """Получает текущую цену товара с Ozon по HTML‑странице"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        price_patterns = [
            {"class": re.compile(r".*price.*", re.I)},
            {"class": "tsBodyL"},
            {"data-widget": "webPrice"},
        ]

        for pattern in price_patterns:
            el = soup.find("span", pattern)
            if not el:
                continue
            text = el.get_text(strip=True)
            digits = re.sub(r"[^\d]", "", text)
            if digits:
                return int(digits)

        print("[WARN] Не удалось найти цену на странице")
        return None
    except Exception as e:
        print(f"[ERROR] Ошибка при получении цены: {e}")
        return None


# === Команды Telegram‑бота ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    keyboard = [
        [InlineKeyboardButton("🔍 Начать мониторинг", callback_data="monitor")],
        [InlineKeyboardButton("📊 Проверить статус", callback_data="status")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Привет! Я помогу тебе отслеживать цены на Ozon.\n\n"
        "📝 Как использовать:\n"
        "1. Отправь команду /monitor\n"
        "2. Отправь ссылку на товар и целевую цену через пробел\n\n"
        "Пример:\n"
        "<code>https://www.ozon.ru/product/... 5000</code>\n\n"
        "или в две строки:",
        parse_mode="HTML",
        reply_markup=reply_markup,
    )


async def monitor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /monitor"""
    await update.message.reply_text(
        "📝 Отправь мне ссылку на товар Ozon и целевую цену через пробел:\n\n"
        "Пример:\n"
        "<code>https://www.ozon.ru/product/... 5000</code>\n\n"
        "или в две строки:",
        parse_mode="HTML",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений с URL и ценой"""
    text = (update.message.text or "").strip()
    chat_id = update.effective_chat.id

    print(f"[DEBUG] Получено сообщение от {chat_id}: {text}")

    parts = text.split()
    url = None
    target_price = None

    for part in parts:
        if "ozon.ru" in part.lower():
            url = part
        elif part.isdigit():
            target_price = int(part)

    if not url:
        await update.message.reply_text(
            "❌ Не нашёл ссылку на Ozon.\n"
            "Отправь ссылку и цену через пробел, например:\n\n"
            "<code>https://www.ozon.ru/product/... 5000</code>",
            parse_mode="HTML",
        )
        return

    if not target_price:
        await update.message.reply_text(
            "❌ Не нашёл целевую цену.\n"
            "Отправь ссылку и цену через пробел, например:\n\n"
            "<code>https://www.ozon.ru/product/... 5000</code>",
            parse_mode="HTML",
        )
        return

    monitors[chat_id] = {"url": url, "target_price": target_price}

    current_price = get_price(url)

    if current_price is None:
        await update.message.reply_text(
            f"⚠️ Мониторинг запущен, но не удалось получить текущую цену.\n\n"
            f"🎯 Целевая цена: {target_price} ₽\n"
            f"🔗 Товар: {url}\n\n"
            f"Буду проверять вручную по запросу!"
        )
    else:
        if current_price <= target_price:
            await update.message.reply_text(
                "🎉 Отлично! Цена уже ниже целевой!\n\n"
                f"💰 Текущая цена: {current_price} ₽\n"
                f"🎯 Целевая цена: {target_price} ₽\n"
                f"🔗 {url}"
            )
        else:
            await update.message.reply_text(
                "✅ Мониторинг запущен!\n\n"
                f"💰 Текущая цена: {current_price} ₽\n"
                f"🎯 Целевая цена: {target_price} ₽\n"
                f"🔗 Товар: {url}\n\n"
                "Я уведомлю тебя, когда цена снизится (если бот запущен)."
            )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status"""
    chat_id = update.effective_chat.id

    if chat_id not in monitors:
        await update.message.reply_text(
            "❌ У тебя нет активного мониторинга.\n"
            "Используй /monitor чтобы начать!"
        )
        return

    monitor = monitors[chat_id]
    current_price = get_price(monitor["url"])

    if current_price is None:
        await update.message.reply_text(
            "⚠️ Не удалось получить текущую цену.\nПопробую позже!"
        )
        return

    if current_price <= monitor["target_price"]:
        await update.message.reply_text(
            "🎉 Цена достигла цели!\n\n"
            f"💰 Текущая цена: {current_price} ₽\n"
            f"🎯 Целевая цена: {monitor['target_price']} ₽\n"
            f"🔗 {monitor['url']}"
        )
    else:
        await update.message.reply_text(
            "📊 Статус мониторинга:\n\n"
            f"💰 Текущая цена: {current_price} ₽\n"
            f"🎯 Целевая цена: {monitor['target_price']} ₽\n"
            f"📉 Разница: {current_price - monitor['target_price']} ₽\n"
            f"🔗 {monitor['url']}"
        )


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stop"""
    chat_id = update.effective_chat.id

    if chat_id in monitors:
        del monitors[chat_id]
        await update.message.reply_text("⏹️ Мониторинг остановлен!")
    else:
        await update.message.reply_text("У тебя нет активного мониторинга.")


# === Telegram Bot (без JobQueue) ===

async def run_telegram_bot():
    """Запуск Telegram‑бота (без фонового JobQueue для Railway)"""
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError(
            "❌ Токен бота не найден!\n"
            "Создайте .env файл или установите переменную окружения BOT_TOKEN"
        )

    app_tg = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CommandHandler("monitor", monitor_command))
    app_tg.add_handler(CommandHandler("status", status_command))
    app_tg.add_handler(CommandHandler("stop", stop_command))
    app_tg.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Telegram бот запущен! (JobQueue отключён на сервере)")

    await app_tg.initialize()
    await app_tg.start()

    try:
        await app_tg.updater.start_polling()
        await asyncio.Event().wait()
    finally:
        await app_tg.updater.stop()
        await app_tg.stop()
        await app_tg.shutdown()


# === Flask запуск в отдельном потоке ===

def run_flask():
    """Запуск Flask API"""
    port = int(os.getenv("PORT", 5000))
    app_flask.run(host="0.0.0.0", port=port, debug=False)


# === Главная функция ===

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("🌐 Flask API запущен на порту 5000")
    print("📍 API доступен по адресу: http://localhost:5000/api/health")

    asyncio.run(run_telegram_bot())
