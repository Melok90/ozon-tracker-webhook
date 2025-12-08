# 🛍️ Ozon Price Tracker - Full Stack

**Полнофункциональная система мониторинга цен на Ozon.ru**

Telegram Mini App + Python Backend + Real-time парсинг

---

## 🎯 Возможности

### Для пользователя:
- ✅ **Telegram Mini App** с современным интерфейсом
- ✅ **Реальный парсинг** цен с Ozon.ru
- ✅ **Автоматические уведомления** при снижении цены
- ✅ **Ручное обновление** цен по клику
- ✅ **Адаптивный дизайн** под светлую/тёмную тему
- ✅ **Офлайн режим** если API недоступен

### Для разработчика:
- ✅ **Flask REST API** для получения цен
- ✅ **Telegram Bot** для уведомлений
- ✅ **Деплой на Railway** за 5 минут
- ✅ **Без базы данных** (LocalStorage + in-memory)
- ✅ **CORS enabled** для Mini App
- ✅ **Полная документация** и чеклист

---

## 📦 Структура проекта

```
ozon-price-tracker-full/
├── bot_with_api.py           # Python: Flask API + Telegram Bot
├── ozon-tracker-api.html     # Frontend: Telegram Mini App
├── requirements-full.txt     # Python зависимости
├── Procfile                  # Railway конфигурация
├── runtime.txt               # Python версия (3.11.6)
├── .env                      # Переменные окружения (НЕ в Git!)
├── .gitignore                # Игнорируемые файлы
├── DEPLOY-GUIDE.md           # Подробная инструкция деплоя
├── ARCHITECTURE.md           # Описание архитектуры
├── CHECKLIST.md              # Чеклист быстрого запуска
└── README.md                 # Этот файл
```

---

## 🚀 Быстрый старт

### 1. Клонируй проект

```bash
git clone https://github.com/твой-username/ozon-tracker-full.git
cd ozon-tracker-full
```

### 2. Настрой переменные окружения

```bash
echo "BOT_TOKEN=твой_токен_от_BotFather" > .env
```

### 3. Локальный запуск (опционально)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-full.txt
python3 bot_with_api.py
```

### 4. Деплой на Railway

Следуй инструкции в **[DEPLOY-GUIDE.md](DEPLOY-GUIDE.md)**

---

## 🏗️ Архитектура

```
User (Telegram)
    ↓
Telegram Mini App (HTML/CSS/JS)
    ↓ HTTP POST
Flask API (Railway)
    ↓ парсинг
Ozon.ru
    ↓ цены
Flask API → Telegram Bot → Notifications
```

Подробнее в **[ARCHITECTURE.md](ARCHITECTURE.md)**

---

## 📚 API Endpoints

### GET /api/health
Проверка работоспособности API

**Response:**
```json
{
  "status": "ok",
  "message": "Ozon Price API is running",
  "timestamp": "2025-11-06T21:00:00"
}
```

### POST /api/price
Получение цены товара с Ozon

**Request:**
```json
{
  "url": "https://www.ozon.ru/product/..."
}
```

**Response:**
```json
{
  "success": true,
  "price": 4500,
  "url": "https://www.ozon.ru/product/...",
  "currency": "RUB",
  "timestamp": "2025-11-06T21:00:00"
}
```

### GET /api/monitors
Получение списка мониторингов пользователя

**Query Params:**
- `user_id` - ID пользователя Telegram

**Response:**
```json
{
  "success": true,
  "monitors": {...},
  "count": 5
}
```

---

## 🤖 Telegram Bot команды

- `/start` - Запуск бота и приветствие
- `/monitor` - Добавить мониторинг товара
- `/status` - Проверить текущий статус мониторинга
- `/stop` - Остановить мониторинг

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.11, Flask 3.0 |
| Bot | python-telegram-bot 21.1 |
| Парсинг | BeautifulSoup4, requests |
| Хостинг | Railway.app |
| Storage | LocalStorage (Frontend), In-memory (Backend) |

---

## 📝 Зависимости

```
python-telegram-bot==21.1
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
flask==3.0.0
flask-cors==4.0.0
```

---

## 🔐 Безопасность

### ✅ Правильно:
- Токен бота в переменных окружения
- `.env` в `.gitignore`
- CORS настроен только для Telegram
- Валидация URL перед парсингом

### ❌ Никогда:
- Не коммитить `.env` в Git
- Не публиковать токен в коде
- Не отключать валидацию входных данных

---

## 💰 Стоимость

### Railway бесплатный план:
- ✅ 500 часов работы в месяц
- ✅ 1GB RAM
- ✅ Автоматический sleep при неактивности
- ✅ Достаточно для персонального использования

---

## 📊 Мониторинг

### Railway Dashboard:
- **Metrics** - CPU/RAM использование
- **Logs** - логи в реальном времени
- **Deployments** - история деплоев

### Логи через CLI:
```bash
railway logs --tail 100
```

---

## 🐛 Troubleshooting

### API недоступен (🔴 офлайн)
1. Проверь логи на Railway
2. Убедись что проект не в режиме sleep
3. Проверь URL в HTML файле

### Бот не отвечает
1. Проверь переменную `BOT_TOKEN` в Railway
2. Перезапусти проект
3. Проверь логи на ошибки

### Цены не обновляются
1. Ozon мог изменить структуру страницы
2. Обнови паттерны парсинга в `get_price()`
3. Проверь User-Agent в headers

Подробнее в **[DEPLOY-GUIDE.md](DEPLOY-GUIDE.md)** раздел "Troubleshooting"

---

## 🔮 Планы развития

- [ ] PostgreSQL для персистентного хранения
- [ ] Redis для кэширования цен
- [ ] Webhook вместо polling для бота
- [ ] Поддержка нескольких товаров на пользователя
- [ ] Графики изменения цен
- [ ] Экспорт истории в CSV
- [ ] Интеграция с другими маркетплейсами

---

## 📄 Лицензия

MIT License - используй как хочешь!

---

## 🤝 Контрибьюция

Pull requests приветствуются! Для крупных изменений сначала открой issue.

---

## 📞 Поддержка

Есть вопросы? Создай issue в GitHub или напиши в Telegram.

---

## 📚 Документация

- **[DEPLOY-GUIDE.md](DEPLOY-GUIDE.md)** - Подробная инструкция деплоя
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Описание архитектуры
- **[CHECKLIST.md](CHECKLIST.md)** - Чеклист быстрого запуска

---

## ⭐ Благодарности

Спасибо:
- Telegram за Mini Apps API
- Railway за бесплатный хостинг
- python-telegram-bot за отличную библиотеку

---

## 📸 Скриншоты

### Telegram Mini App
```
┌────────────────────────┐
│  🛍️ Ozon Price Tracker │
│  Отслеживай реальные   │
│  цены на товары Ozon   │
├────────────────────────┤
│ 🟢 Подключено к API    │
├────────────────────────┤
│ ➕ Добавить мониторинг │
│                        │
│ Ссылка на товар:       │
│ [___________________] │
│                        │
│ Целевая цена (₽):     │
│ [___________________] │
│                        │
│ [Начать отслеживание] │
├────────────────────────┤
│ 📊 Активные мониторинги│
│                        │
│ ┌──────────────────┐  │
│ │ Товар на Ozon    │  │
│ │ 💰 4500 ₽        │  │
│ │ 🎯 4000 ₽        │  │
│ │ [🔄][🔗][🗑️]     │  │
│ └──────────────────┘  │
└────────────────────────┘
```

---

**Готово к использованию! 🚀**

**Star ⭐ этот репозиторий если помог!**