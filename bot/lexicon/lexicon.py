# Vocabulary and messages
LEXICON_RU = {
    'yes': '✅ Да',
    'no': '❌ Нет',
    'cancel': '🚫 Отменить',
}

# User handler messages
USER_LEXICON = {
    # Start command
    "user_start": (
        "🎉 Добро пожаловать в ИИ Редактор!\n\n"
        "🤖 Мощный инструмент для редактирования изображений с помощью ИИ!\n\n"
        "Как использовать:\n"
        "1. 📷Отправьте изображение\n"
        "2. 📝 Опишите, что хотите изменить\n"
        "3. ✨ Получите результат\n\n"
        "Используйте /help для информации"
    ),
    
    # Edit photo button
    "edit_photo_message": "✏️ Отправьте фото",
    
    # Release messages
    "release_features": (
        "🌟 Основные возможности:\n"
        "🤖 ИИ-редактирование изображений\n"
        "📱 Интуитивный интерфейс\n"
        "⚡ Мгновенная обработка\n"
        "🖼️ Высокое качество результата"
    ),
    
    "subscription_options": (
        "💰 Пакеты редактирования:\n\n"
        " ▫️ Старт — 10 фото за 99₽\n\n"
        " ▫️ Стандарт — 25 фото за 199₽\n\n"
        " ⭐️ Премиум — 100 фото за 599₽\n\n"
        " 🔥 Хотите больше? Выбирайте Личный.\n\n"
        "📌 Фото не сгорают и доступны, пока вы их не используете.\n"
    ),
    
    "channel_subscription_required": (
        "🔒 Для использования бота необходимо подписаться на канал!\n\n"
        "Пожалуйста, подпишитесь на наш канал и повторите попытку.\n\n"
        "🔗 Канал: {channel_url}\n\n"
        "После подписки отправьте изображение снова."
    ),


    
    "release_referral": (
        "🤝 Партнерская программа:\n\n"
        "Зарабатывайте, приглашая друзей! Получайте процент от подписок ваших рефералов. "
        "Чем больше вы приглашаете, тем больше зарабатываете! 💰"
    ),
    
    "release_special_offer": (
        "🎁 Специальное предложение:\n\n"
        "При первом использовании получите бонусные монеты для тестирования функций бота! 🎉"
    ),
    
    # Profile
    "user_profile": (
        "**👤 Ваш профиль**\n\n"
        "Доступно {coins} фото\n\n"
        "Приглашайте друзей и зарабатывайте\n"
        "🔗 Реферальная ссылка: `https://t.me/uaieditbot?start={user_hash}`\n"
        "👥 Приглашено друзей: {invited}\n"
        "💵 Заработано с рефералов: {referral_earnings} руб.\n\n"
        "💸 Вывод от 100 руб.\n\n"
        "Вопросы по выводу средств — @aiigot\n"
    ),
    
    # Referrals
    "user_referrals_header": "**👥 Ваши рефералы**\n\n",
    "user_referrals_item": "👤 ID: `{tg_id}` | 💰 Баланс: {coins}\n",
    "user_referrals_empty": "У вас пока нет рефералов 🙁",
    "user_referrals_more": "\n... и ещё {count} 👥",
    
    # Image processing
    "no_subscription": "❌ Нет активной подписки для обработки изображений.",
    "ask_for_image_changes": "✅ Изображение загружено!\n\nОпишите, что хотите изменить:",
    "processing_image": "⏳ Обрабатываю изображение, подождите...",
    "image_processed": "✨ Изображение обработано!\n\n💰 Осталось генераций: {coins}\n\nОтправьте ещё изображения!",
    "buy_subscription": "💳 Для обработки изображений нужна подписка",
    
    # Help
    "user_help": (
        "**❓ Справка**\n\n"
        "🏠 /start - Главное меню\n"
        "👤 /profile - Профиль\n"
        "💰 /balance - Баланс\n"
        "👥 /referrals - Рефералы\n"
        "❓ /help - Помощь"
    ),
}

# Admin handler messages
ADMIN_LEXICON = {
    # Newsletter
    "newsletter_start": "🚀 Создание новой рассылки\n\nВыберите тип медиа для рассылки:",
    "newsletter_media_type_selected": "✅ Выбран тип: {media_type}\n\nТеперь отправьте медиафайл (фото, видео или GIF):",
    "newsletter_text_prompt": "📝 Отправьте текст для рассылки:",
    "newsletter_button_prompt": "🔘 Хотите добавить кнопку с ссылкой?",
    "newsletter_button_text_prompt": "📝 Введите текст кнопки:",
    "newsletter_button_url_prompt": "🔗 Введите URL для кнопки:",
    "newsletter_preview": "👀 Предварительный просмотр рассылки:",
    "newsletter_confirm_send": "📤 Отправить рассылку {count} пользователям?",
    "newsletter_sending": "📤 Рассылка отправляется... Отправлено: {sent}/{total}",
    "newsletter_completed": "✅ Рассылка завершена!\n📤 Отправлено: {sent} пользователям",
    "newsletter_cancelled": "❌ Создание рассылки отменено",
    "newsletter_no_users": "❌ Нет пользователей для рассылки",
    
    # Statistics
    "admin_stats_empty": "❌ Нет пользователей в базе данных",
    "admin_stats_header": "**📊 Статистика системы**\n\n",
    "admin_stats_users": "👥 Всего пользователей: {users_count}\n",
    "admin_stats_total_coins": "💰 Всего монет: {total_coins}\n",
    "admin_stats_avg_coins": "📊 Средний баланс: {avg_coins:.1f}\n",
    
    # Users list
    "admin_users_empty": "❌ Нет зарегистрированных пользователей",
    "admin_users_header": "**👥 Список пользователей** (всего: {count})\n\n",
    "admin_users_item": "{i}. 👤 ID: {tg_id} | 🔐 Хеш: {user_hash} | 💰 Баланс: {coins}\n",
    "admin_users_more": "\n... и еще {count} 👥",
    
    # Help
    "admin_help_header": "🔧 Административные команды\n\n",
    "admin_help_stats": "📈 /admin_stats - Статистика\n",
    "admin_help_newsletter": "📤 /newsletter - Создать рассылку\n",
    "admin_help_download_db": "",
    "admin_help_add_coins": "💰 /add_coins <tg_id> <amount> - Добавить монеты\n",
    "admin_help_subtract_coins": "💸 /subtract_coins <tg_id> <amount> - Списать монеты\n",
    "admin_help_subtract_money": "💵 /subtract_money <tg_id> <amount> - Списать деньги\n📊 /download_users_db - Скачать базу данных пользователей\n",
    "admin_help_add_to_user_fsm": "💰 /add_to_user_fsm - Интерактивное добавление монет\n",
    "admin_help_add_to_user": "💰 /add_to_user <tg_id> <coins> [money] [description] - Добавить монеты/платеж\n",
    "admin_help_set_referral_percentage": "📊 /set_referral_percentage <tg_id|user_hash> <percentage> - Процент реферала\n",
    "admin_help_help": "❓ /admin_help - Справка по командам\n",
    
    # Add coins messages
    "add_coins_usage": "❌ Неправильный формат.\nИспользуйте: /add_coins <tg_id> <amount>\nПример: /add_coins 123456789 100",
    "add_to_user_usage": "❌ Неправильный формат.\nИспользуйте: /add_to_user <tg_id> <coins> [money] [description]\nПримеры:\n/add_to_user 123456789 100              - 100 монет\n/add_to_user 123456789 100 299 \"Базовый пакет\" - с записью платежа",
    "add_to_user_fsm_start": "Введите Telegram ID пользователя:",
    "add_to_user_fsm_tg_id": "Введите количество монет для добавления:",
    "add_to_user_fsm_money": "Введите сумму платежа (0 если не нужно):",
    "add_to_user_fsm_description": "Введите описание платежа (или 'пропустить' для пропуска):",
    "add_to_user_fsm_cancelled": "❌ Операция отменена.",
    "add_to_user_fsm_completed": "✅ Операция успешно завершена!",
    "operation_failed": "❌ Операция не выполнена. Проверьте данные.",
    "add_coins_success": "✅ Добавлено {amount} монет пользователю {tg_id}\n💰 Новый баланс: {new_balance}",
    "subtract_coins_success": "✅ Списано {amount} монет у пользователя {tg_id}\n💰 Новый баланс: {new_balance}",
    "subtract_money_success": "✅ Списано {amount} руб. у пользователя {tg_id}\n💵 Новый заработок: {new_earnings}",
    "subtract_coins_usage": "❌ Неправильный формат.\nИспользуйте: /subtract_coins <tg_id> <amount>\nПример: /subtract_coins 123456789 100",
    "subtract_money_usage": "❌ Неправильный формат.\nИспользуйте: /subtract_money <tg_id> <amount>\nПример: /subtract_money 123456789 100",
    "add_referral_earnings_success": "✅ Добавлено {amount} к заработку с реферальной системы пользователю {tg_id}\n💵 Новый заработок: {new_earnings}",
    "user_invited_by": "🔗 Пользователь {tg_id} приглашен пользователем {referrer_tg_id}",
    "add_transaction_success": "💰 Создана транзакция для пользователя {tg_id}\nСумма: {amount}₽\nОписание: {description}",
    "set_referral_percentage_success": "✅ Установлен процент реферального вознаграждения для пользователя {tg_id}\n📊 Новый процент: {percentage}%\nПредыдущий процент: {old_percentage}%",
    "set_referral_percentage_usage": "❌ Неправильный формат.\nИспользуйте: /set_referral_percentage <tg_id|user_hash> <percentage>\nПример: /set_referral_percentage 123456789 10",
    "user_not_found": "❌ Пользователь с ID/хешем {tg_id} не найден",
}

# Bot commands for menu
LEXICON_COMMANDS = {
    '/start': 'Главное меню',
    '/profile': 'Мой профиль',
    '/balance': 'Проверить баланс',
    '/referrals': 'Мои рефералы',
    '/help': 'Помощь',
    '/howto': 'Как скачать?',
}

# Export combined LEXICON
LEXICON = {
    **LEXICON_RU,
    **USER_LEXICON,
    **ADMIN_LEXICON,
}
