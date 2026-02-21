"""Фильтры для обработчиков aiogram."""
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from db.database import AsyncSessionLocal
from db.requests_db import UserRepository
from config.config import load_config


class IsPrivateChat(BaseFilter):
    """Фильтр для проверки, что сообщение отправлено в личный чат."""

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"


class IsHavePodpiska(BaseFilter):
    """Фильтр для проверки активной подписки пользователя."""

    async def __call__(self, message: Message) -> bool:
        async with AsyncSessionLocal() as session:
            user = await UserRepository.get_user_by_tg_id(
                session, message.from_user.id
            )
            if not user:
                return False
            
            # Проверяем только наличие монет (без проверки времени подписки)
            return user.coins > 0


class AdminFilter(BaseFilter):
    """Фильтр для проверки прав администратора."""

    async def __call__(
        self, event: Union[Message, CallbackQuery], admin_ids: list[int]
    ) -> bool:
        return event.from_user.id in admin_ids


class IsSubscribedToChannel(BaseFilter):
    """Фильтр для проверки подписки пользователя на канал."""

    async def __call__(self, message: Message, bot: Bot) -> bool:
        config = load_config('.env')
        channel_id = config.channal.id
        
        try:
            # Проверяем статус пользователя в канале
            chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
            # Пользователь считается подписанным, если его статус 'member', 'administrator' или 'creator'
            return chat_member.status in ['member', 'administrator', 'creator']
        except Exception:
            # Если возникла ошибка (например, пользователь заблокировал бота или канал не существует),
            # считаем что пользователь не подписан
            return False
