# ✅ Чеклист быстрого запуска

## 📋 Перед началом

- [ ] Есть аккаунт GitHub
- [ ] Есть токен Telegram бота от @BotFather
- [ ] Установлен Git на компьютере

---

## 🚀 Шаг 1: Подготовка (5 минут)

```bash
# 1. Создай папку
mkdir ozon-price-tracker-full
cd ozon-price-tracker-full

# 2. Скопируй файлы из Perplexity:
# - bot_with_api.py
# - ozon-tracker-api.html
# - requirements-full.txt
# - Procfile
# - runtime.txt

# 3. Создай .env
echo "BOT_TOKEN=твой_токен_здесь" > .env

# 4. Создай .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
.env
*.log
venv/
EOF
```

- [ ] Папка создана
- [ ] Файлы скопированы
- [ ] `.env` создан с токеном
- [ ] `.gitignore` создан

---

## 🌐 Шаг 2: GitHub (3 минуты)

```bash
# 1. Инициализируй Git
git init
git add .
git commit -m "Initial commit"

# 2. Создай репозиторий на GitHub.com
# Имя: ozon-tracker-full
# Private/Public на выбор

# 3. Залей код
git branch -M main
git remote add origin https://github.com/твой-username/ozon-tracker-full.git
git push -u origin main
```

- [ ] Git репозиторий создан на GitHub
- [ ] Код залит на GitHub
- [ ] `.env` НЕ залит (проверь!)

---

## 🚂 Шаг 3: Railway (5 минут)

### 3.1 Регистрация
1. Зайди на https://railway.app
2. Sign up через GitHub

- [ ] Аккаунт на Railway создан

### 3.2 Деплой
1. New Project → Deploy from GitHub repo
2. Выбери `ozon-tracker-full`
3. Дождись деплоя (~2-3 минуты)

- [ ] Проект создан на Railway
- [ ] Деплой завершён успешно

### 3.3 Переменные окружения
1. Settings → Variables
2. Add Variable: `BOT_TOKEN` = `твой_токен`

- [ ] Переменная `BOT_TOKEN` добавлена

### 3.4 Получи URL
1. Settings → Domains
2. Generate Domain
3. Скопируй URL (например: `https://ozon-tracker-production.railway.app`)

- [ ] URL получен и скопирован

---

## 🔧 Шаг 4: Обнови HTML (2 минуты)

```bash
# Открой ozon-tracker-api.html
# Найди строку:
const API_BASE_URL = 'https://your-railway-app.railway.app';

# Замени на свой URL:
const API_BASE_URL = 'https://твой-railway-url.railway.app';

# Сохрани и залей на GitHub:
git add ozon-tracker-api.html
git commit -m "Update API URL"
git push
```

- [ ] URL в HTML обновлён
- [ ] Изменения закоммичены
- [ ] Изменения запушены на GitHub

---

## 📱 Шаг 5: Telegram Mini App (3 минуты)

### 5.1 Создай Web App
1. Открой @BotFather в Telegram
2. Отправь `/newapp`
3. Выбери своего бота
4. Название: `Ozon Price Tracker`
5. Описание: `Отслеживание цен на Ozon`
6. **Загрузи файл `ozon-tracker-api.html`**

- [ ] Web App создано через @BotFather
- [ ] HTML файл загружен

---

## ✅ Шаг 6: Тестирование (5 минут)

### 6.1 Проверь API
Открой в браузере:
```
https://твой-railway-url.railway.app/api/health
```

Ожидаемый ответ:
```json
{"status": "ok", "message": "Ozon Price API is running"}
```

- [ ] API отвечает (status: ok)

### 6.2 Проверь Telegram Bot
1. Найди своего бота в Telegram
2. Отправь `/start`
3. Должно прийти приветствие

- [ ] Бот отвечает на команды

### 6.3 Проверь Mini App
1. Открой бота
2. Нажми кнопку Menu
3. Выбери `Ozon Price Tracker`
4. Должно показать: 🟢 Подключено к API

- [ ] Mini App открывается
- [ ] Статус: 🟢 Подключено к API

### 6.4 Проверь парсинг
1. В Mini App добавь любой товар Ozon
2. Укажи целевую цену
3. Нажми "Начать отслеживание"
4. Должна загрузиться реальная цена

- [ ] Товар добавлен
- [ ] Цена загрузилась

---

## 🎉 Готово!

Если все пункты отмечены ✅ — **система работает полностью!**

---

## 🐛 Если что-то не работает:

### API не отвечает (🔴 офлайн)
```bash
# Проверь логи на Railway
railway logs

# Проверь переменные окружения
railway variables
```

### Бот не отвечает
1. Проверь `BOT_TOKEN` в Railway Variables
2. Перезапусти проект на Railway (Deployments → Redeploy)

### Mini App не загружается
1. Проверь URL в `ozon-tracker-api.html`
2. Залей обновлённый файл через @BotFather заново

---

## 📊 Мониторинг:

### Railway Dashboard
- **Metrics** — CPU/RAM
- **Logs** — логи в реальном времени
- **Deployments** — история

### Команды Railway CLI (опционально)
```bash
# Установка
npm i -g @railway/cli

# Логи
railway logs --tail 100

# Статус
railway status
```

---

## 🎯 Следующие шаги:

- [ ] Протестируй с реальным товаром Ozon
- [ ] Настрой уведомления в Telegram
- [ ] Поделись ботом с друзьями
- [ ] Добавь больше товаров для мониторинга

---

**Всё работает? Поздравляю! 🎉🚀**

**Есть вопросы? Пиши в чат! 😊**