from PIL import Image
import pillow_heif
from telebot import types
import telebot
import mimetypes
import sqlite3
import string
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

pillow_heif.register_heif_opener()


def mar_creater():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    btn12 = types.KeyboardButton("Удалить базу данных")
    btn13 = types.KeyboardButton("Назад")
    markup.add(btn2, btn3, btn4, btn5, btn6,
               btn7, btn8, btn9, btn10, btn11, btn12, btn13)
    return markup


def mar_admin():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    markup.add(btn2, btn3, btn4, btn5, btn6,
               btn7, btn8, btn9, btn10, btn11, btn12)
    return markup


def mar_empl():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("Личные данные")
    btn3 = types.KeyboardButton("Изменить должность")
    btn4 = types.KeyboardButton("Изменить имя")
    btn5 = types.KeyboardButton("Задания для меня")
    btn6 = types.KeyboardButton("Выполнить задание")
    btn7 = types.KeyboardButton("Выполненые мною задания")
    btn8 = types.KeyboardButton("Назад")
    markup.add(btn2, btn3, btn4, btn5, btn6, btn7, btn8)
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
# (os.getcwd()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def get_meta(file_path):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument(f'--user-agent={UserAgent().random}')
        brow = webdriver.Chrome(options=options)
        brow.get("https://suip.biz/ru/?act=mat")
        '''if brow.status == 200:
            return "Метаданные невозможно получить из-за ошибки на нашей стороне"'''
        element = WebDriverWait(brow, 8).until(
            EC.presence_of_element_located((By.NAME, 'fileforsending')))
        element.send_keys(file_path)
        element = WebDriverWait(brow, 8).until(
            EC.presence_of_element_located((By.NAME, "Submit1")))
        element.click()
        info = brow.find_element(
            By.CSS_SELECTOR, "pre")
        info = info.text.split("\n")
        infometa = ""
        for arg in info:
            arg = re.sub(r'\s{2,}', ' ', arg)
            arg = arg.split(":")
            if arg[0] == "Дата съёмки ":
                infometa += "Дата съёмки: " + ":".join(arg[1:])[1:] + "\n"
            elif arg[0] == "Компьютер/Система ":
                infometa += "Компьютер/Система: "+arg[1][1:] + "\n"
            elif arg[0] == "GPS – Местоположение ":
                arg[1] = arg[1].replace("deg", "°")
                arg = arg[1].replace(" ", "")
                arg = arg.replace("\"", "")
                infometa += "GPS-link: " + \
                    f"https://www.google.com/maps/place/{arg}"+"\n"
        if infometa == "":
            return "Метаданные не найденны на этом фото, проверьте настройки конфиденциальности камеры"
        return infometa
        brow.quit()
    except Exception as ex:
        # print(ex)
        return "Что-то пошло не так"


def convert_to_jpg(file_path, name):
    try:
        if file_path.split(".")[-1] != "jpg":
            img = Image.open(file_path)
            img.convert('RGB').save(f'{name}.jpg')
            os.remove(file_path)
    except:
        return 1
