from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ".........."
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создание Inline клавиатуры
def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    calculate_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    formulas_button = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    keyboard.add(calculate_button, formulas_button)
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=create_inline_keyboard())

@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (годы) + 5\n"
        "Для женщин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (годы) - 161"
    )
    await bot.send_message(call.from_user.id, formula_message)
    await call.answer()  # Удаляем уведомление о нажатии кнопки

@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()  # Устанавливаем состояние age
    await call.message.answer("Введите свой возраст:")
    await call.answer()  # Удаляем уведомление о нажатии кнопки

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Обновляем данные о возрасте
    await UserState.growth.set()  # Устанавливаем состояние growth
    await message.answer("Введите свой рост:")

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Обновляем данные о росте
    await UserState.weight.set()  # Устанавливаем состояние weight
    await message.answer("Введите свой вес:")

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)  # Обновляем данные о весе
    data = await state.get_data()  # Получаем все данные

    try:
        age = int(data['age'])
        growth = int(data['growth'])
        weight = int(data['weight'])

        # Формула для мужчин
        calories = 10 * weight + 6.25 * growth - 5 * age + 5

        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    except ValueError:
        await message.answer("Ошибка: Введите корректные числовые значения.")

    await state.finish()  # Завершаем состояние


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)