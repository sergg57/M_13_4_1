# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class User_State(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text ='Calories')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await User_State.age.set()

@dp.message_handler(state=User_State.age)
async def set_grow(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await User_State.growth.set()

@dp.message_handler(state=User_State.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await User_State.weight.set()

@dp.message_handler(state=User_State.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    #calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.2 # с учетом активности
    calories = (10 * weight + 6.25 * growth - 5 * age + 5) # упрошенная
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)