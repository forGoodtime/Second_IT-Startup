BvckZ — идея проекта и полный план

(Сохрани как idea.md — это полный рабочий документ: идея, MVP, стек, дорожная карта, задачи, критерии приёма и метрики.)

1. Короткое описание

BvckZ — сервис апсайкла одежды: из 4–5 старых футболок создаём 1–2 новые уникальные вещи с кастомным дизайном (включая национальные орнаменты, мемориальные элементы и брендовые патчи). Сервис сочетает e-commerce, кастомайзер (3D-гардероб в WebApp/Telegram) и эко-логистику (приём и переработка вещей).

Цель MVP: подтвердить спрос и получить первые 50 заявок. Цель продакшн: устойчивый бренд, B2C+B2B каналы, автоматизированное производство и прозрачная цепочка (hash в блокчейн для доверия).

2. Проблема

Люди имеют старую одежду, которая занимает место или выбрасывается.

Нет простого, эстетичного и доверительного пути передать вещи для переработки и получить качественную новую вещь.

Потенциальные покупатели боятся качества апсайкленных изделий и утраты вещей.

3. Решение (кратко)

Онлайн-сервис, который:

принимает старые вещи (пункты приёма / курьер),

визуализирует финальное изделие в 3D (Telegram WebApp + сайт),

шьёт/собирает изделие в мастерской/фабрике,

обеспечивает прозрачность (фото процесса, гарантия, запись хэша события в блокчейн),

продаёт уникальные изделия и даёт бонусы/геймификацию за сдачу вещей.

4. ЦА

Молодёжь 16–35 лет (ориентир) — хотят уникальность.

Эко-активисты; фанаты культуры (орнаменты).

B2B (компании) — апсайкл корпоративных футболок в мерч.

Семьи/клиенты, желающие сохранить память (мемориальная вещь).

5. УТП (value proposition)

Персонализация + апсайкл: из личных вещей — новая, уникальная вещь.

Прозрачность + гарантия: фото процесса, 30-дн гарантия, хэш событий.

Быстрая визуализация в 3D → пользователь уверен в том, что он получит.

6. Функционал (минимум и расширение)
6.1 MVP (обязательное)

Landing (информация + примеры дизайнов).

Регистрация/логин (email или Telegram Login).

WebApp/Telegram mini-app: 3-card preview (центральная футболка + 2 боковые).

Форма заявки на сдачу вещей (адрес/пункт/курьер).

Order-service (создание заказа, статусы).

Media-service: генерация превью (композит mockup).

n8n workflow: форма → создание заказа → уведомление в боте.

Простая админка: список заявок, смена статуса.

БД (Postgres), Docker Compose для локального dev.

Basic analytics (PostHog) + логирование stdout.

MVP Acceptance: 50 собранных заявок или ≥25% CTR по лендингу→заявка (в тесте).

6.2 V1 (после валидации)

Интеграция платежей (Stripe/Kaspi).

3D viewer (glTF/three.js) + вращение/zoom.

Полный рабочий production workflow (приём → производство → доставка).

Ledger hashing (SHA256) + запись Merkle root в Blockchain (Polygon/TON).

Rewards system (баллы за сданные вещи).

Расширенный search (Meilisearch), фильтрация, pagination.

CI/CD, K8s, monitoring (Prometheus/Grafana), logging (Loki).

Load tests (k6), security scans (Trivy, SAST).

7. Технологический стек
MVP стек (быстро стартовать)

Backend: FastAPI (Python)

Frontend: Nuxt 3 (Vue 3) для landing + WebApp

Bot: aiogram (Telegram)

DB: Postgres (docker-compose)

File storage: MinIO (S3 compatible)

Queue/automation: n8n (workflows)

Search: Meilisearch (если нужен)

Analytics: PostHog (events)

Payments: Stripe (test mode)

Dev: Docker Compose, GitHub

Production стек (масштаб)

K8s, Helm, ArgoCD (GitOps)

FastAPI / Go (перформанс критичных)

RabbitMQ / Kafka (events)

Postgres cluster + PgBouncer

Redis (cache, leaderboards)

S3 (Cloud provider) + CDN (Cloudflare)

Prometheus + Grafana + Loki + Jaeger + Sentry

Vault (secrets), OPA (policies)

Blockhain: Polygon (batch merkle root tx)

8. Архитектура (в 3 строчки)

Frontend (Web + Telegram WebApp) ↔ API Gateway ↔ микросервисы (auth, users, products, orders, media, recycle, ledger, notification). Async events через RabbitMQ/Kafka. Media в S3 + CDN. Monitoring + logs in observability stack.

9. Основные API (примеры)

POST /auth/register — {email, password} → 201.

POST /auth/login — {email, password} → {access, refresh}.

POST /donations — {user_id, items[], pickup_method} → {donation_id, status}.

POST /orders — {user_id, items[], delivery} → {order_id, status}.

GET /orders/{id} — status, tracking.

POST /media/render — {design} → {preview_url}.

(Описать OpenAPI для каждого сервиса в openapi.yaml).

10. Данные — базовая модель (high-level)

users(id, name, email, role, tg_id, created_at)

donation_batches(id, user_id, items_count, status, location, created_at)

donation_items(id, batch_id, condition, photo_url)

designs(id, user_id, product_template, metadata(json), preview_url)

orders(id, user_id, status, total_price, payment_id)

ledger_events(id, source, payload_hash, txid, created_at)

11. UX / пользовательский путь (MVP)

Пользователь видит landing → нажимает «Начать» → логин (email или tg).

Открывает WebApp: 3 карточки, кастомизация, preview.

Заполняет заявку на сдачу (адрес/пункт) и делает предзаказ (или оставляет заявку).

Н8Н → создаёт заказ, оповещает бот (status updates).

После производства приходит уведомление + трек/QR для получения.

12. Команда (первые роли)

Бекзат — TeamLead (product, investors, роадмап)

Нұрлыбек — Аналитик (метрики, A/B, отчёты)

Даулет А. — Маркетолог (growth, соцсети)

Даулет Ж. — Операционный менеджер (логистика, QC)

Разработчик(-и) — Backend/Frontend/DevOps (на старте 1–2)

13. Дорожная карта (15 недель по курсу)

(Краткий план, актуализирован по задачам курса — см. подробный roadmap)

W1 — План + architecture + распределение ролей.

W2 — Repo + docker-compose + базовый landing.

W3 — Auth (register/login/roles).

W4 — DB schema + migrations.

W5 — CRUD donation/items + basic order flow.

W6 — Media preview + product-service.

W7–W8 — Frontend: landing + WebApp, адаптивность.

W9 — Admin panel.

W10 — Validation, sorting, pagination, error handling.

W11 — Dockerfiles + compose.

W12 — CI (GitHub Actions).

W13 — Tests + load tests (k6).

W14 — Deploy staging/prod + monitoring (Prometheus/Grafana).

W15 — Final demo + documentation + presentation.

14. Acceptance Criteria (для сдачи / проверки)

Регистрация/аутентификация: рабочая, пароли хранятся хэщировано.

Роли: user/admin разделены и работают.

Основной flow: donation → order → production → delivery (end-to-end).

API: documented OpenAPI, интеграция frontend↔backend.

Docker-compose запускает рабочее окружение.

CI запускает тесты при PR.

Мониторинг basic: /metrics scrape, dashboard latency/error.

Load test: p95 latency < 1s (или согласованное SLO), error <1% при тестовой нагрузке.

15. KPI / метрики успеха

Конверсия лендинг → заявка ≥ 20–30% (MVP goal).

Количество заявок в пилоте: ≥ 50 (MVP).

CR from lead → paid order ≥ 10% (цель).

Повторные клиенты (30 days) ≥ 10% (retention target).

Cost per acquisition (CPA) — отслеживать по месяцам.

16. Маркетинг / GTM (коротко)

Запуск через студенческие Telegram-чаты + TikTok (before/after).

Партнёры: кофейни/магазины как пункты приёма.

Коллаборации с локальными дизайнерами/ремесленниками (орнаменты).

B2B-программа для корпоративных сдач (мерч переработка).

17. Риски и mitigation

Низкое качество готовых изделий → чёткая сортировка, QC, тестовые прототипы.

Логистика дорогая → локальные пункты, франчайзинг мастерских.

Недоверие пользователей → фото/видео процесса, гарантия, ledger hashing.

Юридика (бренды на вещах) → remove logos, require consent for branded items.

18. Оценка стоимости/ресурсов (ориентировочно)

MVP (self-hosted dev + small cloud): $200–800 / мес.

Пилот (1город, небольшое производство): $5k–15k initial (оборудование, аренда, маркет).

Prod (кластеры, SLA, monitoring): $300–1500+/мес + ops costs.

19. План первых шагов (checklist — сделать сейчас)

Создать репо GitHub и положить idea.md.

Инициализировать docker-compose с Postgres, MinIO, Redis, n8n, auth-stub, webapp-stub.

Сделать лендинг + простой WebApp mockup (3 images).

Настроить форму (Typeform/Google) + n8n workflow → create order in DB.

Провести 10 интервью + опрос (ранний traction).

Собирать первые 50 заявок, анализировать.

20. Issues / задачи для первого спринта (разбить в GitHub issues)

 Инициализация репозитория, README, license.

 Docker Compose dev stack.

 Auth-service (register/login + JWT).

 Landing page (hero + CTA).

 WebApp static demo (3-card preview).

 n8n workflow: form → create order.

 DB schema initial + migrations.

 Basic analytics (PostHog) event tracking.

 Conduct 10 user interviews.

21. Документы и артефакты (что положить в репо)

README.md — быстрый старт.

idea.md — этот файл.

infra/docker-compose.yml — dev stack.

services/*/openapi.yaml — API contract.

docs/roadmap.md, docs/runbooks/*.md.

course/templates/weekly_report_template.md — если нужно сдавать отчёты.