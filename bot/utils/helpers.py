"""Вспомогательные функции для работы с пользователями."""

import hashlib
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.requests_db import UserRepository, TransactionRepository


async def generate_user_hash(tg_id: int) -> str:
    return hashlib.sha256(str(tg_id).encode()).hexdigest()[:12]


async def get_or_create_user(
    session: AsyncSession,
    tg_id: int,
    username: Optional[str] = None,
    invited_by_hash: Optional[str] = None,
) -> dict:
    """Получает существующего пользователя или создаёт нового с отслеживанием реферала."""
    user = await UserRepository.get_user_by_tg_id(session, tg_id)

    if not user:
        user_hash = await generate_user_hash(tg_id)

        inviter = None
        if invited_by_hash:
            inviter = await UserRepository.get_user_by_hash(session, invited_by_hash)
            if inviter and inviter.user_hash == user_hash:
                inviter = None

        user = await UserRepository.create_user(
            session=session,
            tg_id=tg_id,
            user_hash=user_hash,
            username=username,
            invited_by_hash=inviter.user_hash if inviter else None,
            coins=1
        )

        if inviter:
            await UserRepository.increment_invited_count(session, inviter.id)

    return {
        "id": user.id,
        "tg_id": user.tg_id,
        "username": user.username,
        "coins": user.coins,
        "user_hash": user.user_hash,
        "invited_count": user.invited_count,
        "invited_by_hash": user.invited_by_hash,
    }


async def process_user_payment(
    session: AsyncSession,
    tg_id: int,
    coins: int,
    money: int = 0,
    description: str = "",
) -> list[str]:
    """Обрабатывает платеж пользователя: добавляет монеты, создает транзакцию и начисляет процент рефералу."""
    user = await UserRepository.get_user_by_tg_id(session, tg_id)
    if not user:
        return []

    operations = []

    # Добавляем монеты пользователю
    if coins != 0:
        u = await UserRepository.add_coins(session, user.id, coins)
        if u:
            operations.append(
                f"✅ Добавлено {coins} монет пользователю {tg_id}\n💰 Новый баланс: {u.coins}"
            )

    # Создаем транзакцию если указана сумма
    if money > 0:
        await TransactionRepository.create_transaction(session, user.id, money, description)
        operations.append(
            f"💰 Создана транзакция для пользователя {tg_id}\nСумма: {money}₽\nОписание: {description}"
        )

    # Начисляем процент рефералу если есть пригласивший
    if money > 0 and user.invited_by_hash:
        referrer = await UserRepository.get_user_by_hash(session, user.invited_by_hash)
        if referrer:
            referral_amount = money * referrer.referral_percentage // 100
            if referral_amount > 0:
                r = await UserRepository.add_referral_earnings(session, referrer.id, referral_amount)
                if r:
                    operations.append(
                        f"✅ Добавлено {referral_amount} к заработку с реферальной системы пользователю {referrer.tg_id}\n💵 Новый заработок: {r.referral_earnings}"
                    )

    return operations
