"""User handlers."""

from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, CallbackQuery

from db.database import AsyncSessionLocal
from db.requests_db import UserRepository, UsageRepository
from lexicon.lexicon import USER_LEXICON
from filters.filters import IsPrivateChat, IsHavePodpiska, IsSubscribedToChannel
from utils.helpers import get_or_create_user
from fsm.fsm import UserState
from service.service import upload_image_to_imgbb, process_image_with_ai, delete_image_from_imgbb
from config.config import load_config
from keyboards.keyboards import get_subscription_keyboard, get_instruction_keyboard, get_main_menu_keyboard

config = load_config('.env')
router = Router(name="user_router")

@router.message(Command("start"), IsPrivateChat())
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    invited_by_hash = message.text.split()[1] if message.text and len(message.text.split()) > 1 else None
    async with AsyncSessionLocal() as session:
        await get_or_create_user(session, message.from_user.id, message.from_user.username, invited_by_hash=invited_by_hash)
    await message.answer(USER_LEXICON["user_start"], parse_mode="Markdown", reply_markup=get_main_menu_keyboard())


@router.message(Command("profile"), IsPrivateChat())
async def cmd_profile(message: types.Message) -> None:
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_user_by_tg_id(session, message.from_user.id)
        if not user:
            await message.answer("Пользователь не найден")
            return
        invited_info = f"Приглашен: {user.invited_by_hash[:12]}..." if user.invited_by_hash else "Приглашен: Нет"
        text = USER_LEXICON["user_profile"].format(
            id=user.id, tg_id=user.tg_id, user_hash=user.user_hash[:12],
            coins=user.coins, invited=user.invited_count, referral_earnings=user.referral_earnings
        ) + f"\n{invited_info}"
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("balance"), IsPrivateChat())
async def cmd_balance(message: types.Message) -> None:
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_user_by_tg_id(session, message.from_user.id)
        if not user:
            await message.answer("Пользователь не найден")
            return
    await message.answer(f"Баланс: {user.coins} монет")


@router.message(Command("referrals"), IsPrivateChat())
async def cmd_referrals(message: types.Message) -> None:
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_user_by_tg_id(session, message.from_user.id)
        if not user:
            await message.answer("Пользователь не найден")
            return
        referrals = await UserRepository.get_user_referrals(session, user.user_hash)
        if not referrals:
            await message.answer(USER_LEXICON["user_referrals_empty"])
            return
        text = USER_LEXICON["user_referrals_header"]
        for r in referrals[:30]:
            text += USER_LEXICON["user_referrals_item"].format(tg_id=r.tg_id, coins=r.coins)
        if len(referrals) > 30:
            text += USER_LEXICON["user_referrals_more"].format(count=len(referrals) - 30)
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("help"), IsPrivateChat())
async def cmd_help(message: types.Message) -> None:
    await message.answer(USER_LEXICON["user_help"], parse_mode="Markdown")


@router.message(Command("howto"), IsPrivateChat())
async def cmd_howto(message: types.Message) -> None:
    """Handle /howto command - show instructions."""
    photo_paths = ["bot/service/photo/1.jpg", "bot/service/photo/2.jpg", "bot/service/photo/3.jpg"]
    media_group = [types.InputMediaPhoto(media=types.FSInputFile(p), caption="📥 Как скачать обработанное фото:\n\n1. Нажмите на изображение, чтобы открыть его\n2. Нажмите кнопку \"Сохранить\" (скалка) в правом верхнем углу\n3. Фото сохранится в вашу галерею" if i == 0 else None) for i, p in enumerate(photo_paths)]
    try:
        await message.answer_media_group(media_group)
    except Exception:
        for i, p in enumerate(photo_paths):
            try:
                await message.answer_photo(types.FSInputFile(p), caption="📥 Как скачать обработанное фото:\n\n1. Нажмите на изображение, чтобы открыть его\n2. Нажмите кнопку \"Сохранить\" (скалка) в правом верхнем углу\n3. Фото сохранится в вашу галерею" if i == 0 else None)
            except Exception:
                continue


@router.message(lambda m: m.content_type == ContentType.PHOTO, IsHavePodpiska(), IsSubscribedToChannel())
async def handle_image(message: types.Message, state: FSMContext, bot: Bot) -> None:
    photo = message.photo[-1]
    await state.update_data(image_file_id=photo.file_id)
    result = await upload_image_to_imgbb(photo.file_id, bot.token, config.bot.imgbb_api, timeout=30)
    if not result:
        await message.answer("Ошибка загрузки изображения.")
        return
    await state.update_data(image_url=result["url"], delete_url=result.get("delete_url"))
    await message.answer(USER_LEXICON["ask_for_image_changes"])
    await state.set_state(UserState.waiting_for_image_prompt)

@router.message(lambda m: m.content_type == ContentType.PHOTO, IsHavePodpiska(), ~IsSubscribedToChannel())
async def handle_image_no_channel_subscription(message: types.Message, state: FSMContext, bot: Bot) -> None:
    """Handle image from users who have subscription but not subscribed to channel."""
    config = load_config('.env')
    channel_url = config.channal.url
    await message.answer(
        USER_LEXICON["channel_subscription_required"].format(channel_url=channel_url), 
        parse_mode="Markdown"
    )

@router.message(UserState.waiting_for_image_prompt, IsPrivateChat(), IsHavePodpiska())
async def handle_image_prompt(message: types.Message, state: FSMContext, bot: Bot) -> None:
    user_prompt = message.text
    await state.update_data(user_prompt=user_prompt)
    data = await state.get_data()
    image_url = data.get("image_url")
    if not image_url:
        await message.answer("Ошибка: изображение не найдено.")
        await state.clear()
        return
    await message.answer(USER_LEXICON["processing_image"])
    processed_url = await process_image_with_ai(image_url, user_prompt, config.bot.polza_api)
    if not processed_url:
        await message.answer("Ошибка обработки изображения.", reply_markup=get_main_menu_keyboard())
        await state.clear()
        return
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_user_by_tg_id(session, message.from_user.id)
        if user and user.coins > 0:
            await UserRepository.subtract_coins(session, user.id, 1)
            await UsageRepository.create_usage(session, user.id, 1)
            user = await UserRepository.get_user_by_tg_id(session, message.from_user.id)
            caption = USER_LEXICON["image_processed"].format(coins=user.coins)
        else:
            caption = USER_LEXICON["image_processed"].format(coins="неизвестно")
    await message.answer_photo(photo=processed_url, caption=caption, reply_markup=get_instruction_keyboard())
    if data.get("delete_url"):
        try:
            await delete_image_from_imgbb(data["delete_url"], timeout=30)
        except Exception as e:
            pass
    await state.clear()


@router.message(IsPrivateChat(), lambda m: m.content_type == ContentType.PHOTO, ~IsHavePodpiska())
async def handle_image_no_subscription(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(USER_LEXICON["subscription_options"], reply_markup=get_subscription_keyboard(), parse_mode="Markdown")


@router.callback_query(lambda c: c.data == "get_instructions")
async def handle_instructions_callback(callback_query: CallbackQuery) -> None:
    photo_paths = ["bot/service/photo/1.jpg", "bot/service/photo/2.jpg", "bot/service/photo/3.jpg"]
    media_group = [types.InputMediaPhoto(media=types.FSInputFile(p), caption="📥 Как скачать обработанное фото:\n\n1. Нажмите на изображение, чтобы открыть его\n2. Нажмите кнопку \"Сохранить\" (скалка) в правом верхнем углу\n3. Фото сохранится в вашу галерею" if i == 0 else None) for i, p in enumerate(photo_paths)]
    try:
        await callback_query.message.answer_media_group(media_group)
    except Exception:
        for i, p in enumerate(photo_paths):
            try:
                await callback_query.message.answer_photo(types.FSInputFile(p), caption="📥 Как скачать обработанное фото:\n\n1. Нажмите на изображение, чтобы открыть его\n2. Нажмите кнопку \"Сохранить\" (скалка) в правом верхнем углу\n3. Фото сохранится в вашу галерею" if i == 0 else None)
            except Exception:
                continue
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "user_profile")
async def handle_profile_callback(callback_query: CallbackQuery) -> None:
    """Handle user_profile button click - show user profile."""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_user_by_tg_id(session, callback_query.from_user.id)
        if not user:
            await callback_query.answer("Пользователь не найден", show_alert=True)
            return
        invited_info = f"Приглашен: {user.invited_by_hash[:12]}..." if user.invited_by_hash else "Приглашен: Нет"
        text = USER_LEXICON["user_profile"].format(
            id=user.id, tg_id=user.tg_id, user_hash=user.user_hash[:12],
            coins=user.coins, invited=user.invited_count, referral_earnings=user.referral_earnings
        ) + f"\n{invited_info}" + "\n\n📷Отправьте изображение"
    
    # Проверяем, отличается ли новое сообщение от текущего
    current_text = callback_query.message.text or callback_query.message.caption
    current_markup = callback_query.message.reply_markup
    
    new_markup = get_main_menu_keyboard()
    
    # Сравниваем текст и количество кнопок в клавиатуре
    text_changed = current_text != text
    markup_changed = True
    
    if current_markup and new_markup:
        # Сравниваем количество строк и кнопок
        if len(current_markup.inline_keyboard) == len(new_markup.inline_keyboard):
            markup_changed = False
            for row_current, row_new in zip(current_markup.inline_keyboard, new_markup.inline_keyboard):
                if len(row_current) != len(row_new):
                    markup_changed = True
                    break
                for btn_current, btn_new in zip(row_current, row_new):
                    if btn_current.text != btn_new.text or btn_current.callback_data != btn_new.callback_data:
                        markup_changed = True
                        break
                if markup_changed:
                    break
    
    # Если текст или клавиатура изменились, редактируем сообщение
    if text_changed or markup_changed:
        try:
            await callback_query.message.edit_text(text, parse_mode="Markdown", reply_markup=new_markup)
        except Exception as e:
            # Если все равно возникает ошибка, просто показываем уведомление
            await callback_query.answer("Вы уже просматриваете профиль", show_alert=True)
    else:
        # Если сообщение не изменилось, просто показываем уведомление
        await callback_query.answer("Вы уже просматриваете профиль", show_alert=True)


@router.callback_query(lambda c: c.data == "edit_photo")
async def handle_edit_photo_callback(callback_query: CallbackQuery) -> None:
    """Handle edit_photo button click - send message to upload photo."""
    await callback_query.answer()
    await callback_query.message.answer(USER_LEXICON["edit_photo_message"])
