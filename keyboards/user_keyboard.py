from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bExpense = KeyboardButton(text='Расход')
bIncome = KeyboardButton(text='Доход')

kbType = [
    [bExpense],
    [bIncome]
]

kb_operation = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=kbType)

bEUR = KeyboardButton(text='EUR')
bRUB = KeyboardButton(text='RUB')
bUSD = KeyboardButton(text='USD')

kbCurrencies = [
    [bEUR],
    [bUSD],
    [bRUB]
]

kb_currencies = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=kbCurrencies)

bASC = KeyboardButton(text="По возрастанию даты")
bDESC = KeyboardButton(text="По убыванию даты")

kbMethods = [
    [bASC],
    [bDESC]
]

kb_methods = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=kbMethods)

bCancel = KeyboardButton(text="Отмена")

kbCancel = [[bCancel]]

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=kbCancel)
