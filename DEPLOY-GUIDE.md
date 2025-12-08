# 🚀 Полная инструкция: Telegram Mini App + Python Backend

## 📦 Структура проекта

```
ozon-price-tracker-full/
├── bot_with_api.py           # Python бот + Flask API
├── ozon-tracker-api.html     # HTML приложение (подключено к API)
├── requirements-full.txt     # Все зависимости
├── Procfile                  # Для Railway/Heroku
├── runtime.txt               # Версия Python
└── .env                      # Переменные окружения (НЕ коммитить!)
```

---

## 🎯 Вариант B: Полная связка (Backend + Frontend)

### ⚙️ Что получаем:
- ✅ **Реальный парсинг цен Ozon** (не демо)
- ✅ **Telegram бот** для уведомлений
- ✅ **Web App** с красивым интерфейсом
- ✅ **API** для связи между ботом и приложением

---

## 📝 Шаг 1: Подготовка файлов

### 1.1 Создай папку проекта

```bash
mkdir ozon-price-tracker-full
cd ozon-price-tracker-full
```

### 1.2 Скопируй файлы в папку:

- `bot_with_api.py` — Python бот с Flask API
- `ozon-tracker-api.html` — HTML приложение
- `requirements-full.txt` — зависимости
- `Procfile` — для деплоя
- `runtime.txt` — версия Python

### 1.3 Создай `.env` файл

```bash
echo "BOT_TOKEN=8325367163:AAF55K3o3GzDfmSHNdMhnVw8627T4ka5BbE" > .env
```

⚠️ Этот файл **НЕ заливаем** на GitHub!

### 1.4 Создай `.gitignore`

```
__pycache__/
*.pyc
.env
*.log
venv/
```

---

## 🚀 Шаг 2: Деплой на Railway.app

### 2.1 Зарегистрируйся на Railway

1. Зайди на https://railway.app
2. Sign up через GitHub

### 2.2 Залей код на GitHub

```bash
cd ozon-price-tracker-full
git init
git add .
git commit -m "Initial commit: Ozon Price Tracker with API"
git branch -M main
git remote add origin https://github.com/<твой-username>/ozon-tracker-full.git
git push -u origin main
```

### 2.3 Создай проект на Railway

1. **New Project** → **Deploy from GitHub repo**
2. Выбери репозиторий `ozon-tracker-full`
3. Railway автоматически обнаружит Python проект

### 2.4 Добавь переменные окружения

В Railway:
- Settings → Variables → Add Variable
- **Name:** `BOT_TOKEN`
- **Value:** `8325367163:AAF55K3o3GzDfmSHNdMhnVw8627T4ka5BbE`

### 2.5 Получи URL приложения

1. Railway задеплоит проект
2. Перейди в **Settings** → **Domains**
3. **Generate Domain** → получишь URL типа:
   ```
   https://ozon-tracker-full-production.railway.app
   ```

**Запиши этот URL! Он понадобится для HTML.**

---

## 🌐 Шаг 3: Настройка HTML приложения

### 3.1 Обнови API URL в HTML файле

Открой `ozon-tracker-api.html` и найди строку:

```javascript
const API_BASE_URL = 'https://your-railway-app.railway.app';
```

Замени на **свой Railway URL**:

```javascript
const API_BASE_URL = 'https://ozon-tracker-full-production.railway.app';
```

### 3.2 Сохрани изменения

```bash
git add ozon-tracker-api.html
git commit -m "Update API URL"
git push
```

---

## 📱 Шаг 4: Создание Telegram Mini App

### 4.1 Создай бота через @BotFather

1. Открой @BotFather в Telegram
2. Отправь `/newbot`
3. Название: `Ozon Price Tracker`
4. Username: `ozon_price_tracker_bot` (или другой уникальный)

✅ Токен уже у тебя есть, он в `.env`

### 4.2 Создай Web App

1. Отправь `/newapp` в @BotFather
2. Выбери своего бота
3. Название приложения: `Ozon Price Tracker`
4. Описание: `Отслеживание цен на Ozon с реальным парсингом`
5. **Загрузи файл `ozon-tracker-api.html`**

🎉 **Готово! Mini App создано!**

---

## 🧪 Шаг 5: Тестирование

### 5.1 Проверь API

Открой в браузере:
```
https://твой-railway-url.railway.app/api/health
```

Должен вернуть:
```json
{
  "status": "ok",
  "message": "Ozon Price API is running",
  "timestamp": "2025-11-06T..."
}
```

### 5.2 Проверь Telegram бота

1. Найди своего бота в Telegram
2. Отправь `/start`
3. Должно прийти приветственное сообщение

### 5.3 Проверь Mini App

1. Открой своего бота
2. Нажми кнопку Menu (возле поля ввода)
3. Выбери `Ozon Price Tracker`
4. Должно открыться приложение с индикатором:
   ```
   🟢 Подключено к API
   ```

---

## ✨ Как это работает:

### Архитектура:

```
Telegram Mini App (HTML)
    ↓ HTTP запросы
Flask API (Railway)
    ↓ парсинг
Ozon.ru
    ↓ цены
Flask API → Telegram Bot → Уведомления пользователю
```

### Флоу работы:

1. **Пользователь** добавляет товар в Mini App
2. **HTML** отправляет POST на `/api/price`
3. **Flask API** парсит Ozon и возвращает цену
4. **HTML** сохраняет мониторинг локально
5. **Telegram бот** проверяет цены каждые 2 часа
6. При снижении цены → **уведомление** в Telegram

---

## 🔧 API Endpoints:

### GET /api/health
Проверка работоспособности
```bash
curl https://your-app.railway.app/api/health
```

### POST /api/price
Получение цены товара
```bash
curl -X POST https://your-app.railway.app/api/price \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.ozon.ru/product/..."}'
```

Ответ:
```json
{
  "success": true,
  "price": 4500,
  "url": "https://www.ozon.ru/product/...",
  "currency": "RUB",
  "timestamp": "2025-11-06T21:00:00"
}
```

---

## 🐛 Troubleshooting:

### Проблема: API недоступен (🔴 офлайн)

**Причины:**
1. Railway приложение не запущено
2. Неверный URL в HTML
3. CORS проблема

**Решение:**
```bash
# Проверь логи на Railway
railway logs

# Проверь URL в HTML
grep "API_BASE_URL" ozon-tracker-api.html
```

### Проблема: Бот не отвечает

**Причины:**
1. Неверный токен
2. Railway приложение остановлено

**Решение:**
1. Проверь переменную `BOT_TOKEN` в Railway
2. Перезапусти проект на Railway

### Проблема: Цены не обновляются

**Причины:**
1. Ozon заблокировал парсинг
2. Изменилась структура страницы

**Решение:**
Обнови паттерны парсинга в функции `get_price()` в `bot_with_api.py`

---

## 📊 Мониторинг:

### Railway Dashboard:
- **Metrics** — загрузка CPU/RAM
- **Logs** — логи приложения в реальном времени
- **Deployments** — история деплоев

### Логи приложения:
```bash
railway logs --tail 100
```

---

## 💰 Стоимость:

### Railway бесплатный план:
- ✅ 500 часов в месяц (~20 дней)
- ✅ Автоматический sleep при неактивности
- ✅ 1GB RAM
- ✅ 1GB хранилище

**Достаточно для персонального использования!**

---

## 🔐 Безопасность:

### ✅ ОБЯЗАТЕЛЬНО:
- Токен бота только в переменных окружения
- `.env` в `.gitignore`
- Приватный GitHub репозиторий (опционально)

### ❌ НИКОГДА:
- Не коммить `.env` в Git
- Не публиковать токен в коде
- Не передавать токен третьим лицам

---

## 🎉 Итог:

Теперь у тебя полнофункциональная система:

1. ✅ **Python бот** — Telegram уведомления
2. ✅ **Flask API** — реальный парсинг Ozon
3. ✅ **Mini App** — красивый интерфейс
4. ✅ **Деплой** — работает 24/7 на Railway

**Всё готово к использованию! 🚀**

---

## 📞 Дополнительные ресурсы:

- Railway Docs: https://docs.railway.app
- Telegram Bot API: https://core.telegram.org/bots
- Telegram Mini Apps: https://core.telegram.org/bots/webapps

---

**Вопросы? Пиши! Помогу с настройкой! 😊**