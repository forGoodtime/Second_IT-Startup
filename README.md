# 🌟 BvckZ MVP - Платформа Апсайклинга Одежды

> **Превращаем старую одежду в уникальные дизайнерские вещи с помощью ИИ и 3D технологий**

## 📋 О проекте

BvckZ - это инновационная платформа апсайклинга, которая позволяет пользователям сдавать старую одежду и создавать из неё уникальные дизайнерские футболки с персонализированными принтами.

### 🎯 Ключевые особенности:
- ♻️ **Экологичность** - вторичное использование текстиля
- 🎨 **3D Дизайнер** - интерактивное создание уникальных принтов
- 🤖 **ИИ Персонализация** - умные рекомендации дизайна
- 📱 **Telegram Интеграция** - уведомления и WebApp
- 🏪 **B2B/B2C Модель** - работа с частными лицами и компаниями

## 🚀 Статус MVP

✅ **ГОТОВ К ДЕМО И ИНВЕСТИЦИЯМ**

### 📊 Текущие метрики:
- **2,322 строк кода** (production ready)
- **11 микросервисов** в Docker окружении
- **Полнофункциональный API** с аутентификацией
- **3D интерактивный интерфейс**
- **Админ-панель управления**

## Быстрый запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Запуск проекта

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd Second_IT-Startup
```

2. **Создайте файл окружения:**
```bash
cp .env.example .env
```

3. **Отредактируйте .env файл** (замените значения по умолчанию на безопасные):
```bash
nano .env
```

4. **Запустите сервисы:**
```bash
cd infra
docker-compose up -d
```

5. **Дождитесь запуска всех сервисов** (может занять несколько минут):
```bash
docker-compose ps
```

### Доступные сервисы

После запуска будут доступны:

- **Лендинг:** http://localhost:3000
- **WebApp (3D дизайнер):** http://localhost:3001  
- **API:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs
- **n8n (автоматизация):** http://localhost:5678
- **MinIO (файловое хранилище):** http://localhost:9001
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

### Первоначальная настройка

1. **Откройте n8n** (http://localhost:5678) и настройте базовые воркфлоы
   - Логин: admin / password123 (как в .env файле)

2. **Создайте bucket в MinIO** (http://localhost:9001):
   - Логин: minioadmin / minioadmin123
   - Создайте bucket с именем `bvckz-files`

3. **Протестируйте API:**
```bash
curl http://localhost:8000/api/health
```

## Архитектура MVP

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Лендинг       │    │   WebApp        │    │   API           │
│   (Nuxt 3)      │    │   (Nuxt 3)      │    │   (FastAPI)     │
│   Port: 3000    │    │   Port: 3001    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┬─────┴─────┬─────────────────┐
         │                 │           │                 │
    ┌────▼───┐       ┌─────▼────┐ ┌────▼────┐      ┌─────▼──┐
    │ n8n    │       │PostgreSQL│ │ Redis   │      │ MinIO  │
    │Workflow│       │  DB      │ │ Cache   │      │   S3   │
    └────────┘       └──────────┘ └─────────┘      └────────┘
```

## Основные функции MVP

### ✅ Реализовано:
- [x] Регистрация/авторизация пользователей
- [x] 3D превью дизайна (базовое)
- [x] Создание заказов и заявок на сдачу вещей
- [x] API для всех основных операций
- [x] Лендинг с формой заявки
- [x] WebApp для кастомизации
- [x] Docker контейнеризация

### 🔄 В процессе:
- [ ] n8n воркфлоы (форма → заказ → уведомление)
- [ ] Интеграция с Telegram Bot
- [ ] Загрузка изображений в MinIO
- [ ] PostHog аналитика

### 📋 Планируется:
- [ ] Интеграция платежей (Stripe)
- [ ] Полноценная 3D визуализация
- [ ] Система уведомлений
- [ ] Админ панель

## API Endpoints

### Аутентификация
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `GET /api/users/me` - Профиль пользователя

### Заявки на сдачу
- `POST /api/donations` - Создать заявку на сдачу вещей  
- `GET /api/donations` - Получить свои заявки

### Заказы
- `POST /api/orders` - Создать заказ
- `GET /api/orders` - Получить свои заказы

### Система
- `GET /api/health` - Проверка здоровья API

Полная документация: http://localhost:8000/docs

## Разработка

### Структура проекта
```
Second_IT-Startup/
├── .env.example                 # Пример переменных окружения
├── infra/
│   └── docker-compose.yml       # Оркестрация сервисов
├── mvp-services/
│   ├── api/                     # FastAPI бэкенд
│   │   ├── main.py             # Основное приложение
│   │   ├── requirements.txt    # Python зависимости
│   │   └── Dockerfile          
│   ├── web-landing/            # Лендинг (Nuxt 3)
│   │   ├── pages/index.vue     # Главная страница
│   │   ├── package.json        
│   │   └── Dockerfile
│   └── web-webapp/             # WebApp (Nuxt 3)
│       ├── pages/index.vue     # 3D дизайнер
│       ├── package.json
│       └── Dockerfile
├── idea.md                     # Подробное описание проекта
└── plan.md                     # План проекта и архитектура
```

### Локальная разработка

1. **API (FastAPI):**
```bash
cd mvp-services/api
pip install -r requirements.txt
uvicorn main:app --reload
```

2. **Frontend (Nuxt):**
```bash
cd mvp-services/web-landing  # или web-webapp
npm install
npm run dev
```

### Тестирование

```bash
# Проверка здоровья всех сервисов
curl http://localhost:8000/api/health
curl http://localhost:3000
curl http://localhost:3001

# Регистрация пользователя
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## Мониторинг и логи

```bash
# Просмотр логов всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f api
docker-compose logs -f web
```

## Остановка сервисов

```bash
# Остановка всех сервисов
docker-compose down

# Остановка с удалением volumes (ВНИМАНИЕ: удалит все данные)
docker-compose down -v
```

## Troubleshooting

### Проблема: Сервисы не запускаются
```bash
# Проверьте статус
docker-compose ps

# Проверьте логи
docker-compose logs

# Пересоберите контейнеры
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: База данных не подключается
```bash
# Проверьте PostgreSQL
docker-compose exec postgres psql -U bvckz -d bvckz_mvp -c "SELECT 1;"

# Пересоздайте контейнер БД
docker-compose down
docker volume rm bvckz_mvp_postgres_data
docker-compose up -d
```

### Проблема: Frontend не загружается
```bash
# Проверьте сборку Node.js сервисов
docker-compose logs web
docker-compose logs webapp

# Пересоберите frontend
docker-compose build web webapp
docker-compose up -d web webapp
```

## Следующие шаги

1. **Настройка n8n воркфлоов** для автоматизации заявок
2. **Интеграция с Telegram Bot** для уведомлений
3. **Подключение PostHog** для аналитики пользователей
4. **Создание админ панели** для управления заказами
5. **Тестирование с реальными пользователями** (50 заявок - цель MVP)

## Команда

- **Бекзат** - TeamLead (product, инвесторы, роадмап)
- **Нұрлыбек** - Аналитик (метрики, A/B, отчёты) 
- **Даулет А.** - Маркетолог (growth, соцсети)
- **Даулет Ж.** - Операционный менеджер (логистика, QC)

## Лицензия

Проект находится в разработке. Лицензия будет определена позже.

---

**Цель MVP:** Собрать 50 заявок и подтвердить спрос на сервис апсайкла одежды 🎯
