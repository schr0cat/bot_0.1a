from aiogram import types, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.database.postgres import DataBase


async def cmd_user(message: types.Message, state: FSMContext):
    check_user = await DataBase.execute(
        "SELECT id, telegram_id FROM tg_users WHERE telegram_id = $1",
        message.from_user.id,
        fetch=True
    )
    # check_name = await DataBase.execute(
    #     "SELECT first_name FROM tg_users WHERE first_name = $1",
    #     get_data['first_name'],
    #     fetch=True
    # )
    if not check_user:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Отменить действие",
            callback_data="cancel")
        )
        await message.answer(
            "Здравствуйте. Я бот Салют. Давайте познакомимся ;)\n\nВведите своё имя, пожалуйста:",
            reply_markup=builder.as_markup()
        )
        await state.set_state(RegisterUserState.waiting_for_first_name)
    else:
        await message.answer(f"Ваш аккаунт уже зарегистрирован, его телеграм id: {check_user[0]['telegram_id']}")
        # await message.answer(f"Здравствуйте, {check_name[0]['first_name']}")


class RegisterUserState(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_age = State()


async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Действие отменено")
    await callback.answer()


async def first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить действие",
        callback_data="cancel")
    )

    await message.answer(
        "Введите вашу фамилию:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(RegisterUserState.waiting_for_last_name)


async def last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить действие",
        callback_data="cancel")
    )

    await message.answer(
        "Введите ваш возраст:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(RegisterUserState.waiting_for_age)


async def age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Отменить действие",
            callback_data="cancel")
        )
        await message.answer("Возраст вводится только числом !", reply_markup=builder.as_markup())
    else:
        await state.update_data(age=message.text)
        get_data = await state.get_data()

        await DataBase.execute(
            "INSERT INTO tg_users(telegram_id, first_name, last_name, age) VALUES($1, $2, $3, $4)",
            message.from_user.id,
            get_data['first_name'],
            get_data['last_name'],
            int(get_data['age']),
            execute=True
        )
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Да", callback_data="profile_yes"))
        builder.add(types.InlineKeyboardButton(text="Нет", callback_data="profile_no"))
        await message.answer("Хотите вывести информацию о профиле ?", reply_markup=builder.as_markup())


async def cmd_input_info(callback: types.CallbackQuery, state: FSMContext):
    get_data = await state.get_data()
    await callback.message.answer(
        f"Имя: {get_data['first_name']}\n"
        f"Фамилия: {get_data['last_name']}\n"
        f"Возраст: {get_data['age']}"
    )
    await callback.answer()
    await state.set_state(None)


async def cmd_no_info(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы успешно зарегистрировались в боте Salut !")
    await state.set_state(None)


def register_states_handler(router: Router):
    router.message.register(first_name, state=RegisterUserState.waiting_for_first_name)
    router.message.register(last_name, state=RegisterUserState.waiting_for_last_name)
    router.message.register(age, state=RegisterUserState.waiting_for_age)
    router.message.register(cmd_cancel, state="*")
    router.callback_query.register(cmd_input_info, state="*")
    router.callback_query.register(cmd_no_info, state="*")
