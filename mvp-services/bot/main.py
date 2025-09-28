import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
import os
import json
import aiohttp

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
API_BASE = os.getenv("API_BASE", "http://api:8000/api")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:3001")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def start_command(message: Message):
    """Handle /start command"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌟 Открыть дизайнер",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Мои заявки",
                    callback_data="my_donations"
                ),
                InlineKeyboardButton(
                    text="📦 Мои заказы", 
                    callback_data="my_orders"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ О проекте",
                    callback_data="about"
                )
            ]
        ]
    )
    
    await message.answer(
        f"🌟 Добро пожаловать в BvckZ!\n\n"
        f"Превратите старую одежду в уникальные изделия с национальными орнаментами.\n\n"
        f"Как это работает:\n"
        f"1. Сдайте 4-5 старых футболок\n"
        f"2. Создайте дизайн в 3D редакторе\n"
        f"3. Получите готовое уникальное изделие\n\n"
        f"Нажмите кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )

@router.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command"""
    help_text = (
        "🤖 Команды бота BvckZ:\n\n"
        "/start - Главное меню\n"
        "/help - Справка\n"
        "/status - Статус системы\n"
        "/donate - Создать заявку на сдачу вещей\n"
        "/orders - Мои заказы\n\n"
        "📱 Используйте веб-приложение для создания дизайна и заказов!"
    )
    await message.answer(help_text)

@router.message(Command("status"))
async def status_command(message: Message):
    """Check system status"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE}/health") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.answer(
                        f"✅ Система работает нормально\n"
                        f"Статус: {data.get('status', 'unknown')}\n"
                        f"Время: {data.get('timestamp', 'unknown')}"
                    )
                else:
                    await message.answer("❌ API недоступен")
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        await message.answer("❌ Ошибка при проверке статуса")

@router.message(Command("donate"))
async def donate_command(message: Message):
    """Create donation request via bot"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Создать заявку через WebApp",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    
    await message.answer(
        "📋 Создание заявки на сдачу вещей\n\n"
        "Используйте веб-приложение для создания заявки:\n"
        "• Укажите количество вещей\n"  
        "• Выберите способ передачи\n"
        "• Создайте дизайн будущего изделия\n",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "my_donations")
async def my_donations_callback(callback):
    """Show user's donations"""
    await callback.answer()
    
    # Here we would integrate with API to get user's donations
    # For now, show placeholder
    await callback.message.edit_text(
        "📋 Ваши заявки:\n\n"
        "Для просмотра заявок войдите в веб-приложение.\n"
        "В будущих версиях эта информация будет доступна прямо в боте!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
            ]
        )
    )

@router.callback_query(F.data == "my_orders") 
async def my_orders_callback(callback):
    """Show user's orders"""
    await callback.answer()
    
    await callback.message.edit_text(
        "📦 Ваши заказы:\n\n"
        "Для просмотра заказов войдите в веб-приложение.\n"
        "Здесь будет отображаться статус производства ваших изделий!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
            ]
        )
    )

@router.callback_query(F.data == "about")
async def about_callback(callback):
    """Show about info"""
    await callback.answer()
    
    await callback.message.edit_text(
        "ℹ️ О проекте BvckZ\n\n"
        "🌍 Миссия: Превращение старой одежды в уникальные изделия\n"
        "♻️ Экология: Уменьшаем текстильные отходы\n"
        "🎨 Культура: Национальные орнаменты и дизайн\n"
        "💎 Уникальность: Каждое изделие неповторимо\n\n"
        "📱 MVP версия - протестируйте и оставьте обратную связь!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
            ]
        )
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback):
    """Back to main menu"""
    await callback.answer()
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌟 Открыть дизайнер",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Мои заявки",
                    callback_data="my_donations"
                ),
                InlineKeyboardButton(
                    text="📦 Мои заказы", 
                    callback_data="my_orders"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ О проекте",
                    callback_data="about"
                )
            ]
        ]
    )
    
    await callback.message.edit_text(
        f"🌟 Добро пожаловать в BvckZ!\n\n"
        f"Превратите старую одежду в уникальные изделия с национальными орнаментами.\n\n"
        f"Как это работает:\n"
        f"1. Сдайте 4-5 старых футболок\n"
        f"2. Создайте дизайн в 3D редакторе\n"
        f"3. Получите готовое уникальное изделие\n\n"
        f"Нажмите кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )

# Webhook endpoint for notifications from API
async def webhook_handler(request):
    """Handle webhooks from main API"""
    try:
        data = await request.json()
        event_type = data.get('type')
        payload = data.get('payload', {})
        
        logger.info(f"Received webhook: {event_type}")
        
        if event_type == 'donation_created':
            user_id = payload.get('telegram_id')
            if user_id:
                await bot.send_message(
                    user_id,
                    f"✅ Заявка создана!\n"
                    f"ID: {payload.get('donation_id')}\n"
                    f"Количество вещей: {payload.get('items_count')}\n"
                    f"Способ передачи: {payload.get('pickup_method')}\n\n"
                    f"Мы свяжемся с вами в течение 24 часов!"
                )
        
        elif event_type == 'order_status_changed':
            user_id = payload.get('telegram_id')
            if user_id:
                status_messages = {
                    'paid': '💰 Оплата получена! Заказ передан в производство.',
                    'production': '🏭 Ваше изделие создается в мастерской!',
                    'shipped': '📦 Заказ отправлен! Скоро получите уведомление о доставке.',
                    'completed': '🎉 Заказ завершён! Спасибо за использование BvckZ!'
                }
                
                message = status_messages.get(payload.get('status'), 'Статус заказа изменился')
                await bot.send_message(
                    user_id,
                    f"📋 Обновление заказа #{payload.get('order_id')}\n\n{message}"
                )
        
        return web.json_response({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return web.json_response({'error': str(e)}, status=400)

# Add router to dispatcher
dp.include_router(router)

async def main():
    """Main function"""
    logger.info("Starting Telegram Bot...")
    
    # Create webhook app
    app = web.Application()
    app.router.add_post('/webhook', webhook_handler)
    
    # Start polling (for development)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
