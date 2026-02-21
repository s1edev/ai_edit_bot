from datetime import datetime
from typing import Optional

from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Transaction, Usage

class UserRepository:
    """CRUD операции для User."""

    @staticmethod
    async def create_user(
        session: AsyncSession,
        tg_id: int,
        user_hash: str,
        username: Optional[str] = None,
        invited_by_hash: Optional[str] = None,
        coins: int = 2,
    ) -> User:
        """Создать нового пользователя."""
        user = User(
            tg_id=tg_id,
            username=username,
            user_hash=user_hash,
            invited_by_hash=invited_by_hash,
            coins=coins,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_hash(session: AsyncSession, user_hash: str) -> Optional[User]:
        """Получить пользователя по хешу."""
        result = await session.execute(select(User).where(User.user_hash == user_hash))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, **kwargs) -> Optional[User]:
        """Обновить данные пользователя."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def add_coins(session: AsyncSession, user_id: int, amount: int) -> Optional[User]:
        """Добавить монеты пользователю."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.coins += amount
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def add_referral_earnings(session: AsyncSession, user_id: int, amount: int) -> Optional[User]:
        """Добавить заработок с реферальной системы пользователю."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.referral_earnings += amount
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_referral_percentage(session: AsyncSession, user_id: int, percentage: int) -> Optional[User]:
        """Обновить процент реферального вознаграждения пользователя."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.referral_percentage = percentage
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def subtract_coins(session: AsyncSession, user_id: int, amount: int) -> Optional[User]:
        """Вычесть монеты у пользователя."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.coins -= amount
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def subtract_referral_earnings(session: AsyncSession, user_id: int, amount: int) -> Optional[User]:
        """Вычесть заработок с рефералов у пользователя."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.referral_earnings -= amount
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def increment_invited_count(session: AsyncSession, user_id: int) -> Optional[User]:
        """Увеличить счетчик приглашенных."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return None

        user.invited_count += 1
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> bool:
        """Удалить пользователя."""
        user = await UserRepository.get_user_by_id(session, user_id)
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User]:
        """Получить всех пользователей."""
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_users_count(session: AsyncSession) -> int:
        """Получить количество пользователей."""
        result = await session.execute(select(User))
        return len(result.scalars().all())

    @staticmethod
    async def get_user_referrals(session: AsyncSession, user_hash: str) -> list[User]:
        """Получить всех рефералов пользователя по его хешу."""
        result = await session.execute(
            select(User).where(User.invited_by_hash == user_hash)
        )
        return result.scalars().all()


class TransactionRepository:
    """CRUD операции для Transaction."""

    @staticmethod
    async def create_transaction(
        session: AsyncSession,
        user_id: int,
        amount: int,
        description: str,
    ) -> Transaction:
        """Создать новую транзакцию."""
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            description=description,
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction

    @staticmethod
    async def get_transaction_by_id(
        session: AsyncSession, transaction_id: int
    ) -> Optional[Transaction]:
        """Получить транзакцию по ID."""
        result = await session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_transactions(
        session: AsyncSession, user_id: int, limit: int = 50
    ) -> list[Transaction]:
        """Получить транзакции пользователя."""
        result = await session.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(desc(Transaction.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def delete_transaction(session: AsyncSession, transaction_id: int) -> bool:
        """Удалить транзакцию."""
        transaction = await TransactionRepository.get_transaction_by_id(session, transaction_id)
        if not transaction:
            return False

        await session.delete(transaction)
        await session.commit()
        return True

    @staticmethod
    async def get_user_balance(session: AsyncSession, user_id: int) -> int:
        """Получить баланс пользователя по транзакциям."""
        result = await session.execute(
            select(Transaction).where(Transaction.user_id == user_id)
        )
        transactions = result.scalars().all()
        return sum(t.amount for t in transactions)

    @staticmethod
    async def get_all_transactions(session: AsyncSession) -> list[Transaction]:
        """Получить все транзакции."""
        result = await session.execute(select(Transaction))
        return result.scalars().all()


class UsageRepository:
    """CRUD операции для Usage."""

    @staticmethod
    async def create_usage(
        session: AsyncSession,
        user_id: int,
        coins_used: int,
    ) -> Usage:
        """Создать запись использования."""
        usage = Usage(
            user_id=user_id,
            coins_used=coins_used,
        )
        session.add(usage)
        await session.commit()
        await session.refresh(usage)
        return usage

    @staticmethod
    async def get_usage_by_id(session: AsyncSession, usage_id: int) -> Optional[Usage]:
        """Получить запись использования по ID."""
        result = await session.execute(select(Usage).where(Usage.id == usage_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_usage(
        session: AsyncSession, user_id: int, limit: int = 50
    ) -> list[Usage]:
        """Получить историю использования пользователя."""
        result = await session.execute(
            select(Usage)
            .where(Usage.user_id == user_id)
            .order_by(desc(Usage.used_at))
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_total_coins_used(session: AsyncSession, user_id: int) -> int:
        """Получить общее количество использованных монет."""
        result = await session.execute(
            select(Usage).where(Usage.user_id == user_id)
        )
        usage_records = result.scalars().all()
        return sum(u.coins_used for u in usage_records)

    @staticmethod
    async def get_usage_stats(
        session: AsyncSession, user_id: int, days: int = 7
    ) -> dict:
        """Получить статистику использования за период."""
        from datetime import datetime, timedelta

        start_date = datetime.utcnow() - timedelta(days=days)
        result = await session.execute(
            select(Usage).where(
                and_(Usage.user_id == user_id, Usage.used_at >= start_date)
            )
        )
        usage_records = result.scalars().all()
        return {
            "period_days": days,
            "total_usages": len(usage_records),
            "total_coins_used": sum(u.coins_used for u in usage_records),
            "average_per_usage": (
                sum(u.coins_used for u in usage_records) / len(usage_records)
                if usage_records
                else 0
            ),
        }

    @staticmethod
    async def delete_usage(session: AsyncSession, usage_id: int) -> bool:
        """Удалить запись использования."""
        usage = await UsageRepository.get_usage_by_id(session, usage_id)
        if not usage:
            return False

        await session.delete(usage)
        await session.commit()
        return True

    @staticmethod
    async def get_all_usage(session: AsyncSession) -> list[Usage]:
        """Получить все записи использования."""
        result = await session.execute(select(Usage))
        return result.scalars().all()
