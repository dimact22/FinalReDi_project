from telebot import types
import telebot
import sqlite3
import string
import random
import os


def mar_creater():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В разроботке")
    btn2 = types.KeyboardButton("Cотрудники")
    btn3 = types.KeyboardButton("Удалить сотрудника")
    btn4 = types.KeyboardButton("Добавить админа")
    btn5 = types.KeyboardButton("Убрать админа")
    btn6 = types.KeyboardButton("Личные данные")
    btn7 = types.KeyboardButton("Изменить должность")
    btn8 = types.KeyboardButton("Изменить имя")
    btn9 = types.KeyboardButton("Создать задание")
    btn10 = types.KeyboardButton("Мои задания")
    btn11 = types.KeyboardButton("Задания выполненые сотрудниками")
    btn12 = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6,
               btn7, btn8, btn9, btn10, btn11, btn12)
    return markup


def mar_admin():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В разроботке")
    btn2 = types.KeyboardButton("Cотрудники")
    btn3 = types.KeyboardButton("Личные данные")
    btn4 = types.KeyboardButton("Изменить должность")
    btn5 = types.KeyboardButton("Изменить имя")
    btn6 = types.KeyboardButton("Создать задание")
    btn7 = types.KeyboardButton("Мои задания")
    btn8 = types.KeyboardButton("Задания для меня")
    btn9 = types.KeyboardButton("Выполнить задание")
    btn10 = types.KeyboardButton("Выполненые мною задания")
    btn11 = types.KeyboardButton("Задания выполненые сотрудниками")
    btn12 = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6,
               btn7, btn8, btn9, btn10, btn11, btn12)
    return markup


def mar_empl():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В разроботке")
    btn2 = types.KeyboardButton("Личные данные")
    btn3 = types.KeyboardButton("Изменить должность")
    btn4 = types.KeyboardButton("Изменить имя")
    btn5 = types.KeyboardButton("Задания для меня")
    btn6 = types.KeyboardButton("Выполнить задание")
    btn7 = types.KeyboardButton("Выполненые мною задания")
    btn8 = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return markup


def get_names_of_database(folder_path=''):
    DB_names = []
    if folder_path != '':
        file_names = os.listdir(folder_path)
    else:
        file_names = os.listdir()
    for file in file_names:
        file = file.split(".")
        if file[-1] == "db":
            DB_names.append(file[:-1][0])
    return DB_names


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
