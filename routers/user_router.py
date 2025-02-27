import prettytable as pt
from operator import itemgetter

import psycopg2
from telegram.constants import ParseMode
import requests
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import dbqueries
from keyboards.user_keyboard import kb_operation, kb_methods, kb_currencies, kb_cancel


def form_table(data):  # красивое оформление таблицы с помощью библиотеки prettyTable
    table = pt.PrettyTable(['Дата', 'Сумма', 'ID пользователя', 'Тип операции'])
    table.align['Дата'] = 'l'
    table.align['Сумма'] = 'm'
    table.align['ID пользователя'] = 'm'
    table.align[
        'Тип операции'] = 'r'
    table_data = []
    for i in range(len(data)):
        table_data.append((data[i][0].strftime("%d-%m-%Y"), float(data[i][1]), str(data[i][2]),
                           str(data[i][3])))
    for date, amount, id, type in table_data:
        table.add_row([date, f"{amount:.2f}", id, type])  # добавляем в табличку строку
    return table  # возвращаем готовую таблицу на вывод


class FSMStates(StatesGroup):
    enter_name = State()
    choosing_type = State()
    enter_amount = State()
    enter_date = State()
    select_method = State()
    select_currency = State()


router = Router()


@router.message(F.text.lower() == 'отмена') # нажатие кнопки "Отмена"
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Действие было отменено!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("reg"))  # команда /reg
async def register(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if dbqueries.check_user(user_id):
        login = dbqueries.get_name(user_id)
        await message.answer(str(login) + ", вы уже зарегистрированы!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Начало процесса регистрации.\nПожалуйста, введите Ваш логин:", reply_markup=kb_cancel)
        await state.set_state(FSMStates.enter_name)


@router.message(FSMStates.enter_name)  # этап ввода логина
async def enter_name(message: types.Message, state: FSMContext):
    login = message.text
    dbqueries.add_user(message.from_user.id, login)
    await message.answer(f"Добро пожаловать на борт, {login}!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("add_operation"))  # команда /add_operation
async def add_operation(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if dbqueries.check_user(user_id):
        await message.answer("Пожалуйста, выберите тип операции: ", reply_markup=kb_operation)
        await state.set_state(FSMStates.choosing_type)
    else:
        await message.answer("Пожалуйста, сперва пройдите процесс регистрации! (используйте команду /reg)")


@router.message(FSMStates.choosing_type, F.text.lower() == 'расход')  # тип операции "расход"
async def choose_expense(message: types.Message, state: FSMContext):
    await state.update_data(choosing_type='расход')
    await message.answer("Пожалуйста, введите сумму операции (в рублях):", reply_markup=kb_cancel)
    await state.set_state(FSMStates.enter_amount)


@router.message(FSMStates.choosing_type, F.text.lower() == 'доход')  # тип операции "доход"
async def choose_income(message: types.Message, state: FSMContext):
    await state.update_data(choosing_type='доход')
    await message.answer("Пожалуйста, введите сумму операции (в рублях):", reply_markup=kb_cancel)
    await state.set_state(FSMStates.enter_amount)


@router.message(FSMStates.enter_amount)  # этап ввода суммы операции
async def enter_amount(message: types.Message, state: FSMContext):
    if message.text.replace(".", "").isnumeric():
        await state.update_data(enter_amount=float(message.text))
        await message.answer("Пожалуйста, введите дату операции (DD/MM/YYYY):", reply_markup=kb_cancel)
        await state.set_state(FSMStates.enter_date)
    else:
        await message.answer("Неправильные входные данные, пожалуйста, попробуйте снова!",
                             reply_markup=ReplyKeyboardRemove())


@router.message(FSMStates.enter_date)  # этап ввода даты операции
async def enter_date(message: types.Message, state: FSMContext):
    date = str(message.text)
    data = await state.get_data()
    op_type = data['choosing_type']
    amount = data['enter_amount']
    try:
        dbqueries.add_operation(date, amount, message.from_user.id, op_type)
    except psycopg2.Error:
        await message.answer("Что-то пошло не так, пожалуйста, перепроверьте введенные данные и попробуйте снова!",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Операция была успешно добавлена!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("operations"))  # команда /operations
async def oper_list(message: types.Message, state: FSMContext):
    if dbqueries.check_user(message.from_user.id):
        await message.answer("Пожалуйста, выберите метод сортировки (относительно даты):", reply_markup=kb_methods)
        await state.set_state(FSMStates.select_method)
    else:
        await message.answer("Пожалуйста, сперва пройдите процесс регистрации! (используйте команду /reg)")


@router.message(FSMStates.select_method, F.text.lower() == 'по возрастанию даты')
@router.message(FSMStates.select_method, F.text.lower() == 'по убыванию даты')  # этап выбора метода сортировки
async def oper_list(message: types.Message, state: FSMContext):
    if message.text.lower() == 'по возрастанию даты':
        await state.update_data(select_method='ASC')
    else:
        await state.update_data(select_method='DESC')
    await message.answer("Выберите отображаемую валюту:", reply_markup=kb_currencies)
    await state.set_state(FSMStates.select_currency)


@router.message(FSMStates.select_currency, F.text.lower() == 'eur')
@router.message(FSMStates.select_currency, F.text.lower() == 'usd')  # перевод рублей в другую валюту
async def list_another(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    data = dbqueries.select_operations(chat_id)
    r = requests.get('http://195.58.54.159:8000/rate', params={
        'currency': message.text.upper()})
    if r.ok:
        rate = r.json()['rate']
        sort_method = (await state.get_data())['select_method']
        if sort_method.lower() == 'asc':
            data.sort(key=itemgetter(0),
                      reverse=False)
        elif sort_method.lower() == 'desc':
            data.sort(key=itemgetter(0), reverse=True)
        for i in range(len(data)):
            data[i] = (data[i][0], data[i][1] / rate, data[i][2],
                       data[i][3])
        table = form_table(
            data)
        await message.answer(f"Список операций (выбранная валюта: {message.text.upper()}):")
        await message.answer(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Непредвиденная ошибка на сервере, пожалуйста, попробуйте позже!",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router.message(FSMStates.select_currency,
                F.text.lower() == 'rub')  # вывод без перевода 
async def list_our(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    data = dbqueries.select_operations(chat_id)
    sort_method = (await state.get_data())['select_method']
    if sort_method.lower() == 'asc':
        data.sort(key=itemgetter(0), reverse=False)
    elif sort_method.lower() == 'desc':
        data.sort(key=itemgetter(0), reverse=True)
    table = form_table(data)
    await message.answer("Список операций (выбранная валюта: RUB):")
    await message.answer(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    await state.clear()
