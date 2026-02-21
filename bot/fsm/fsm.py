"""Состояния конечного автомата (FSM) для управления диалогом."""

from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    """Состояния диалога обычных пользователей."""
    waiting_for_image_prompt = State()


class AdminState(StatesGroup):
    """Состояния диалога администраторов."""
    add_to_user_tg_id = State()
    add_to_user_coins = State()
    add_to_user_money = State()
    add_to_user_description = State()
    newsletter_media_type = State()
    newsletter_media_content = State()
    newsletter_text = State()
    newsletter_button_text = State()
    newsletter_button_url = State()
