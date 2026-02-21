"""Клавиатуры для взаимодействия с пользователями."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с кнопками для покупки подписки."""
    buttons = [
        [
            InlineKeyboardButton(text="⭐️ 100 фото", url="https://t.me/aiigot?text=ИИ Редактор 100/599", style="success"),
            InlineKeyboardButton(text="🔥 Личный", url="https://t.me/aiigot?text=ИИ Редактор Кастом", style="primary"),
        ],
        [
            InlineKeyboardButton(text="10 фото", url="https://t.me/aiigot?text=ИИ Редактор 10/99"),
            InlineKeyboardButton(text="25 фото", url="https://t.me/aiigot?text=ИИ Редактор 25/199"),
            
        ],
        [InlineKeyboardButton(text="📄 Пользовательское соглашение", url="https://telegra.ph/Polzovatelskoe-soglashenie-02-11-36")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_instruction_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой для получения инструкций."""
    buttons = [
        [InlineKeyboardButton(text="Как скачать?", callback_data="get_instructions")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="user_profile")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру главного меню с кнопкой профиля."""
    buttons = [
        [InlineKeyboardButton(text="✏️ Редактировать фото", callback_data="edit_photo")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="user_profile")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_newsletter_media_type_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для выбора типа медиа для рассылки."""
    buttons = [
        [
            InlineKeyboardButton(text="📷 Фото", callback_data="media_type_photo"),
            InlineKeyboardButton(text="🎥 Видео", callback_data="media_type_video"),
        ],
        [
            InlineKeyboardButton(text="🎞️ GIF", callback_data="media_type_gif"),
            InlineKeyboardButton(text="📝 Только текст", callback_data="media_type_text"),
        ],
        [InlineKeyboardButton(text="🚫 Отмена", callback_data="cancel_newsletter")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_newsletter_buttons_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для настройки кнопки в рассылке."""
    buttons = [
        [
            InlineKeyboardButton(text="✅ Добавить кнопку", callback_data="add_button"),
            InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip_button"),
        ],
        [InlineKeyboardButton(text="🚫 Отмена", callback_data="cancel_newsletter")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_newsletter_preview_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру для подтверждения отправки рассылки."""
    buttons = [
        [
            InlineKeyboardButton(text="📤 Отправить", callback_data="send_newsletter"),
            InlineKeyboardButton(text="✏️ Изменить", callback_data="edit_newsletter"),
        ],
        [InlineKeyboardButton(text="🚫 Отмена", callback_data="cancel_newsletter")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
