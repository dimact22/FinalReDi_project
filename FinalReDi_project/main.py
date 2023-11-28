from functiontg import *
from functionbd import *
TOKEN = os.environ('TOKEN')
botTimeWeb = telebot.TeleBot(TOKEN)


def update_job_title_in_bd_enter(message, db):
    if message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую", reply_markup=markup)
    else:
        conn = sqlite3.connect(f"{db}.db")
        cur = conn.cursor()
        Bd = FunkBd('userid_name')
        cur.execute(
            f"Insert into users values('{message.from_user.id}','{Bd.get_name_by_id(message.from_user.id)}','Employer', '{message.text}', '{message.from_user.username}')")
        conn.commit()
        conn.close()
        markup = mar_empl()
        botTimeWeb.send_message(
            message.chat.id, text=f"Вы успешно вошли в базу данных {db}, можете продолжать вашу роботу", reply_markup=markup)
        if not Bd.check_execute_database_or_not(message.from_user.id, db):
            Bd.add_database(message.from_user.id, db)
        Bd.set_cur_bd(message.from_user.id, db)


def update_job_title_in_bd_create(message):
    if message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую", reply_markup=markup)
    else:
        random_symbolsdb = generate_random_string(5)
        conn = sqlite3.connect(f'{random_symbolsdb}.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid TEXT PRIMARY KEY,
        name TEXT,
        status TEXT,
        job_title TEXT,
        link TEXT);
        """)
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS completed_tasks(
            task_id INTEGER PRIMARY KEY,
            text TEXT)
            """)
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id TEXT,
        to_id TEXT,
        title TEXT,
        text TEXT,
        pass_or_not INTEGER);
        """)
        conn.commit()
        Bd = FunkBd('userid_name')
        cur.execute(
            f"Insert into users values('{message.from_user.id}','{Bd.get_name_by_id(message.from_user.id)}','Creater', '-','{message.from_user.username}')")
        conn.commit()
        Bd.set_cur_bd(message.from_user.id, random_symbolsdb)
        Bd.add_database(message.from_user.id, random_symbolsdb)
        cur.execute(
            f"update users set job_title = '{message.text}' where userid = '{message.from_user.id}'")
        conn.commit()
        conn.close()
        markup = mar_creater()
        botTimeWeb.send_message(
            message.chat.id, f"Ваши базы данных были успешно созданы, ваш код для входа в эту базу данных: {random_symbolsdb}. По этому коду к вам могут добавляться новые сотрудники. Вы записаны создателем этих баз, и имеете полный контроль над ними.", reply_markup=markup)


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name}</b>, Привет!\nЯ бот который поможет тебе производить правильный менеджмент в твоем бизнесе"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать Базу")
    btn2 = types.KeyboardButton("Войти")
    btn3 = types.KeyboardButton("Изменить мое имя")
    markup.add(btn1, btn2, btn3)
    botTimeWeb.send_message(message.chat.id, first_mess,
                            parse_mode='html', reply_markup=markup)
    botTimeWeb.send_message(
        message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую")


@botTimeWeb.message_handler(commands=['register'])
def set_info(message):
    Bd = FunkBd('userid_name')
    if str(message.from_user.id) not in Bd.get_id_of_users():
        empty_button = telebot.types.ReplyKeyboardRemove()
        msg = botTimeWeb.send_message(
            message.chat.id, "Введите ваше полное имя (Пупкин Иван Инванович) для добавления вашего имя в базу данных", reply_markup=empty_button)
        botTimeWeb.register_next_step_handler(msg, set_info)
    else:
        empty_button = telebot.types.ReplyKeyboardRemove()
        botTimeWeb.send_message(
            message.chat.id, "Вы уже зарегестрированны, но вы можете поменять свои личные данные с помощью кнопки 'Изменить имя'", reply_markup=empty_button)


def set_info(message):
    Bd = FunkBd('userid_name')
    Bd.add_new_user(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать Базу")
    btn2 = types.KeyboardButton("Войти")
    btn3 = types.KeyboardButton("Изменить мое имя")
    markup.add(btn1, btn2, btn3)
    botTimeWeb.send_message(
        message.chat.id, "Регистрация прошла успешно, теперь вы можете работать с базами данных", reply_markup=markup)


def change_my_jt(message):
    conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
    cur = conn.cursor()
    cur.execute(
        f"Update users set job_title = '{message.text}' where userid = '{message.chat.id}';")
    conn.commit()
    conn.close()
    botTimeWeb.send_message(
        message.chat.id, "Ваша должность была изменена, возвращайтесь в главное меню")


def change_my_name(message):
    conn = sqlite3.connect('userid_name.db')
    cur = conn.cursor()
    cur.execute(
        f"Update user_name set name = '{message.text}' where user_id = '{message.chat.id}';")
    conn.commit()
    all_database = cur.execute(
        f"Select name_base from id_databases where user_id = '{message.chat.id}';")
    all_database = all_database.fetchall()
    all_database = list(map(lambda x: x[0], all_database))
    conn.close()
    for base in all_database:
        conn = sqlite3.connect(f'{base}.db')
        cur = conn.cursor()
        cur.execute(
            f"Update users set name = '{message.text}' where userid = '{message.chat.id}';")
        conn.commit()
        conn.close()
    botTimeWeb.send_message(
        message.chat.id, "Вашe имя было измененно во всех базах данных, возвращайтесь в главное меню")


def change_my_name2(message):
    conn = sqlite3.connect('userid_name.db')
    cur = conn.cursor()
    cur.execute(
        f"Update user_name set name = '{message.text}' where user_id = '{message.chat.id}';")
    conn.commit()
    all_database = cur.execute(
        f"Select name_base from id_databases where user_id = '{message.chat.id}';")
    all_database = all_database.fetchall()
    all_database = list(map(lambda x: x[0], all_database))
    conn.close()
    for base in all_database:
        conn = sqlite3.connect(f'{base}.db')
        cur = conn.cursor()
        cur.execute(
            f"Update users set name = '{message.text}' where userid = '{message.chat.id}';")
        conn.commit()
        conn.close()
    botTimeWeb.send_message(
        message.chat.id, "Вашe имя было измененно во всех базах данных, возвращайтесь назад")


def create_task1(message, id_em):
    if message.text == "Главное меню":
        if FunkBd.cr_or_not(message.from_user.id):
            markup = mar_creater()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    else:
        msg = botTimeWeb.send_message(
            message.chat.id, text=f"Теперь введите текст описывающий задание")
        botTimeWeb.register_next_step_handler(
            message, create_task2, id_em=id_em, title=message.text)


def create_task2(message, id_em, title):
    if message.text == "Главное меню":
        if FunkBd.cr_or_not(message.from_user.id):
            markup = mar_creater()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить файлы")
        btn2 = types.KeyboardButton("Выставить задание")
        btn3 = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3)
        msg = botTimeWeb.send_message(
            message.chat.id, "Выберете дальнейшее действие из кнопок", reply_markup=markup)
        botTimeWeb.register_next_step_handler(
            message, create_task3, id_em=id_em, title=title, m_text=message.text)


def create_task3(message, id_em, title, m_text):
    if message.text == "Главное меню":
        conn = sqlite3.connect(f'{FunkBd.cur_bd(message.from_user.id)}.db')
        cur = conn.cursor()
        max_task_id = cur.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = 'tasks'")
        max_task_id = list(max_task_id)
        conn.close()
        if len(max_task_id) == 0:
            max_task_id = 1
        else:
            max_task_id = max_task_id[0][0]+1
        conn.close()
        for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
            file_s = file.split("-")
            if file_s[0] == str(max_task_id):
                os.remove(str(FunkBd.cur_bd(message.from_user.id)) + "cr" +
                          "\\" + file)
        if FunkBd.cr_or_not(message.from_user.id):
            markup = mar_creater()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    elif message.text == "Выставить задание":
        conn = sqlite3.connect(f'{FunkBd.cur_bd(message.from_user.id)}.db')
        cur = conn.cursor()
        cur.execute(
            f"Insert into tasks values(NULL,'{message.from_user.id}','{id_em}', '{title}','{m_text}', 1)")
        conn.commit()
        conn.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        botTimeWeb.send_message(
            message.chat.id, "Ваше задание было успешно выставленно, возвращайтесь в главное меню", reply_markup=markup)
        botTimeWeb.send_message(
            id_em, f"Вам пришло новое задание из базы данных {FunkBd.cur_bd(message.from_user.id)}")
    elif message.text == "Добавить файлы":
        empty_button = telebot.types.ReplyKeyboardRemove()
        msg = botTimeWeb.send_message(
            message.chat.id, "Добавляйте файлы\nБот принимает только файлы(фото так-же отправлять именно файлом)\nВидео любого формата бот не принимает", reply_markup=empty_button)
        botTimeWeb.register_next_step_handler(
            message, add_file, id_em=id_em, title=title, m_text=m_text)


def completed_task(message, id_task):
    if message.text == "Главное меню":
        if FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_empl()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить файлы")
        btn2 = types.KeyboardButton("Выполнить задание")
        btn3 = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3)
        msg = botTimeWeb.send_message(
            message.chat.id, "Текст записан. Теперь выберете дальнейшее действие из кнопок", reply_markup=markup)
        botTimeWeb.register_next_step_handler(
            message, completed_task2, id_task=id_task, text=message.text)


def completed_task2(message, id_task, text):
    if message.text == "Главное меню":
        for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"completed"):
            file_s = file.split("-")
            if file_s[0] == str(id_task):
                os.remove(str(FunkBd.cur_bd(message.from_user.id)) + "completed" +
                          "\\" + file)
        if FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_empl()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    elif message.text == "Выполнить задание":
        conn = sqlite3.connect(f'{FunkBd.cur_bd(message.from_user.id)}.db')
        cur = conn.cursor()
        cur.execute(
            f"Insert into completed_tasks values('{id_task}','{text}')")
        conn.commit()
        cur.execute(
            f"Update tasks set pass_or_not = 0 where task_id = {id_task}")
        conn.commit()
        conn.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        botTimeWeb.send_message(
            message.chat.id, "Ваше задание было успешно сделанно, возвращайтесь в главное меню", reply_markup=markup)
    elif message.text == "Добавить файлы":
        empty_button = telebot.types.ReplyKeyboardRemove()
        msg = botTimeWeb.send_message(
            message.chat.id, "Добавляйте файлы\nБот принимает только файлы(фото так-же отправлять именно файлом)\nВидео любого формата бот не принимает", reply_markup=empty_button)
        botTimeWeb.register_next_step_handler(
            message, add_file_task, id_task=id_task, text=text)


@botTimeWeb.message_handler(content_types=['document', 'photo', 'audio', 'voice'])
def add_file_task(message, id_task, text):
    try:
        if message.document.file_name.split(".")[-1].lower() in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Добавить файлы")
            btn2 = types.KeyboardButton("Выполнить задание")
            btn3 = types.KeyboardButton("Главное меню")
            markup.add(btn1, btn2, btn3)
            botTimeWeb.send_message(
                message.chat.id, "Вы отправили неверный файл нажмите кнопку добавить файл или выставите задание без файлов", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                message, completed_task2, id_task=id_task, text=text)
        else:
            file_info = botTimeWeb.get_file(message.document.file_id)
            downloaded_file = botTimeWeb.download_file(file_info.file_path)
            os.makedirs(
                f'{FunkBd.cur_bd(message.from_user.id)+"completed"}', exist_ok=True)
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.from_user.id)}.db')
            cur = conn.cursor()
            file_path = str(FunkBd.cur_bd(message.from_user.id)) + "completed" + \
                "\\" + f"{id_task}-" + \
                message.document.file_name
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            # if message.document.mime_type.startswith('image'):
                # get_exif('4-IMG_4427.HEIC', "info.txt")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Добавить файлы")
            btn2 = types.KeyboardButton("Выполнить задание")
            btn3 = types.KeyboardButton("Главное меню")
            markup.add(btn1, btn2, btn3)
            botTimeWeb.send_message(
                message.chat.id, "Ваш файл сохранен, добавьте еще файлы нажав кнопку добавить файлы или выставите ваше задание", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                message, completed_task2, id_task=id_task, text=text)
            conn.close()
    except Exception as inst:
        print(inst)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить файлы")
        btn2 = types.KeyboardButton("Выполнить задание")
        btn3 = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, "Вы отправили неверный файл нажмите кнопку добавить файл или выставите задание без файлов", reply_markup=markup)
        botTimeWeb.register_next_step_handler(
            message, completed_task2, id_task=id_task, text=text)


@botTimeWeb.message_handler(content_types=['document', 'photo', 'audio', 'voice'])
def add_file(message, id_em, title, m_text):
    try:
        if message.document.file_name.split(".")[-1].lower() in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Добавить файлы")
            btn2 = types.KeyboardButton("Выставить задание")
            btn3 = types.KeyboardButton("Главное меню")
            markup.add(btn1, btn2, btn3)
            botTimeWeb.send_message(
                message.chat.id, "Вы отправили неверный файл нажмите кнопку добавить файл или выставите задание без файлов", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                message, create_task3, id_em=id_em, title=title, m_text=m_text)
        else:
            file_info = botTimeWeb.get_file(message.document.file_id)
            downloaded_file = botTimeWeb.download_file(file_info.file_path)
            os.makedirs(
                f'{FunkBd.cur_bd(message.from_user.id)+"cr"}', exist_ok=True)
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.from_user.id)}.db')
            cur = conn.cursor()
            max_task_id = cur.execute(
                "SELECT seq FROM sqlite_sequence WHERE name = 'tasks'")
            max_task_id = list(max_task_id)
            if len(max_task_id) == 0:
                file_path = str(FunkBd.cur_bd(message.from_user.id)) + "cr" + \
                    "\\" + "1-"+message.document.file_name
            else:
                file_path = str(FunkBd.cur_bd(message.from_user.id)) + "cr" + \
                    "\\" + f"{max_task_id[0][0]+1}-" + \
                    message.document.file_name
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Добавить файлы")
            btn2 = types.KeyboardButton("Выставить задание")
            btn3 = types.KeyboardButton("Главное меню")
            markup.add(btn1, btn2, btn3)
            botTimeWeb.send_message(
                message.chat.id, "Ваш файл сохранен, добавьте еще файлы нажав кнопку добавить файлы или выставите ваше задание", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                message, create_task3, id_em=id_em, title=title, m_text=m_text)
            conn.close()
    except Exception as inst:
        # print(inst)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить файлы")
        btn2 = types.KeyboardButton("Выставить задание")
        btn3 = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, "Вы отправили неверный файл нажмите кнопку добавить файл или выставите задание без файлов", reply_markup=markup)
        botTimeWeb.register_next_step_handler(
            message, create_task3, id_em=id_em, title=title, m_text=m_text)


@botTimeWeb.message_handler(content_types=['text'])
def func(message):
    Bd = FunkBd('userid_name')
    if (message.text == "Создать Базу"):
        if str(message.from_user.id) not in Bd.get_id_of_users():
            botTimeWeb.send_message(
                message.chat.id, "Для добавления вас в базу данних вам требуется зарегистрироваться, введите команду /register")
        if str(message.from_user.id) in Bd.get_id_of_users():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            random_symbols = generate_random_string(5)
            msg = botTimeWeb.send_message(
                message.chat.id, f"Для продолжения роботы, пожалуйста введите следующие символы: {random_symbols}.", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                msg, create_database, random_symbols=random_symbols)
    elif (message.text == "Войти"):
        if str(message.from_user.id) not in Bd.get_id_of_users():
            botTimeWeb.send_message(
                message.chat.id, "Для добавления вас в базу данних вам требуется зарегистрироваться, введите команду /register")
        if str(message.from_user.id) in Bd.get_id_of_users():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            msg = botTimeWeb.send_message(
                message.chat.id, "Введите код состоящий из 7 цифр для входа в определенную базу данних", reply_markup=markup)
            botTimeWeb.register_next_step_handler(msg, switch_emp_to_BD)
    elif (message.text == "Главное меню"):
        if FunkBd.cr_or_not(message.from_user.id):
            markup = mar_creater()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        elif FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
            markup = mar_admin()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_empl()
            botTimeWeb.send_message(
                message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    elif (message.text == "Cотрудники"):
        if FunkBd.cr_or_not(message.chat.id) or FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            emp = cur.execute("Select * from users")
            count = 0
            for em in emp:
                if em[0] != str(message.chat.id):
                    count += 1
                    msg = botTimeWeb.send_message(
                        message.chat.id, f"Имя: {em[1]}\nСтатус: {em[2]}\nДолжность: {em[3]}\nСсылка: https://t.me/{em[4]}")
            if count == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данный момент у вас нет сотрудников")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Личные данные"):
        conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
        cur = conn.cursor()
        emp = list(cur.execute(
            f"Select * from users where userid = '{message.chat.id}'"))
        botTimeWeb.send_message(
            message.chat.id, f"Имя: {emp[0][1]}\nСтатус: {emp[0][2]}\nДолжность: {emp[0][3]}")
        conn.close()
    elif (message.text == "Изменить должность"):
        keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = btn1 = types.KeyboardButton("Главное меню")
        keyboard2.add(btn1)
        botTimeWeb.send_message(
            message.chat.id, "Пожалуйста подтвердите что вы действительно хотите изменить вашу должность.", reply_markup=keyboard2)
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Да", callback_data=f"change_pers_data")
        button2 = types.InlineKeyboardButton(
            text="Нет", callback_data=f"main_menu")
        keyboard.add(button1, button2)
        botTimeWeb.send_message(
            message.chat.id, "Вы уверенны что хотите изменить вашу должность?", reply_markup=keyboard)
    elif (message.text == "Изменить имя"):
        keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = btn1 = types.KeyboardButton("Главное меню")
        keyboard2.add(btn1)
        botTimeWeb.send_message(
            message.chat.id, "Пожалуйста подтвердите что вы действительно хотите изменить ваше имя", reply_markup=keyboard2)
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Да", callback_data=f"change_name")
        button2 = types.InlineKeyboardButton(
            text="Нет", callback_data=f"main_menu")
        keyboard.add(button1, button2)
        botTimeWeb.send_message(
            message.chat.id, "Вы уверенны что хотите изменить ваше имя?", reply_markup=keyboard)
    elif (message.text == "Изменить мое имя"):
        Bd = FunkBd('userid_name')
        if str(message.from_user.id) not in Bd.get_id_of_users():
            botTimeWeb.send_message(
                message.chat.id, "Для добавления вас в базу данних вам требуется зарегистрироваться, введите команду /register")
        else:
            keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            keyboard2.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Пожалуйста подтвердите что вы действительно хотите изменить ваше имя", reply_markup=keyboard2)
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text="Да", callback_data=f"change_name2")
            button2 = types.InlineKeyboardButton(
                text="Нет", callback_data=f"main_menu2")
            keyboard.add(button1, button2)
            botTimeWeb.send_message(
                message.chat.id, "Вы уверенны что хотите изменить ваше имя?", reply_markup=keyboard)
    elif (message.text == "Добавить админа"):
        if FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            emp = cur.execute("Select * from users")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Главное меню")
            markup.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Добавьте админом сотрудника из списка ниже:", reply_markup=markup)
            count = 0
            for em in emp:
                if em[0] != str(message.chat.id) and not FunkBd.admin_or_not(message.from_user.id, em[0]):
                    count += 1
                    keyboard = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(
                        text="✅Добавить админом✅", callback_data=f"add_admin_user:{em[0]}:{FunkBd.cur_bd(message.chat.id)}")
                    keyboard.add(button1)
                    botTimeWeb.send_message(
                        message.chat.id, f"Имя: {em[1]}\nСтатус: {em[2]}\nДолжность: {em[3]}\nСсылка: https://t.me/{em[4]}", reply_markup=keyboard)
            conn.close()
            if count == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет сотрудников которых можно сделать админами")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Создать задание"):
        if FunkBd.cr_or_not(message.chat.id) or FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            emp = cur.execute("Select * from users")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Главное меню")
            markup.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Добавьте задание сотруднику ниже:", reply_markup=markup)
            count = 0
            for em in emp:
                if em[0] != str(message.chat.id) and not FunkBd.cr_or_not(em[0]):
                    count += 1
                    keyboard = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(
                        text="✅Добавить задание✅", callback_data=f"add_task:{em[0]}")
                    keyboard.add(button1)
                    botTimeWeb.send_message(
                        message.chat.id, f"Имя: {em[1]}\nСтатус: {em[2]}\nДолжность: {em[3]}\nСсылка: https://t.me/{em[4]}", reply_markup=keyboard)
            conn.close()
            if count == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет сотрудников которым можно дать задание")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Задания для меня"):
        if not FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            tasks = cur.execute(
                f"Select * from tasks where to_id = '{message.chat.id}' and pass_or_not = 1;")
            tasks = list(tasks)
            botTimeWeb.send_message(
                message.chat.id, "Задания для вас данны ниже:")
            if len(tasks) == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет заданий")
                conn.close()
            else:
                botTimeWeb.send_message(
                    message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
                for task in tasks:
                    Bd = FunkBd('userid_name')
                    botTimeWeb.send_message(
                        message.chat.id, f"Задание: {task[3]}\nТекст задания: {task[4]}\nСоздатель: {Bd.get_name_by_id(task[1])}")
                    for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
                        file_s = file.split("-")
                        if file_s[0] == str(task[0]):
                            botTimeWeb.send_document(
                                message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"cr"+'\\'+file, 'rb'))
                    botTimeWeb.send_message(
                        message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Мои задания"):
        if FunkBd.cr_or_not(message.chat.id) or FunkBd.admin_or_not(message.chat.id, message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            tasks = cur.execute(
                f"Select * from tasks where from_id = '{message.chat.id}' and pass_or_not = 1;")
            tasks = list(tasks)
            botTimeWeb.send_message(
                message.chat.id, "Все ваши задания данны ниже:")
            if len(tasks) == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент нет заданий созданых вами")
                conn.close()
            else:
                botTimeWeb.send_message(
                    message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
                for task in tasks:
                    Bd = FunkBd('userid_name')
                    botTimeWeb.send_message(
                        message.chat.id, f"Задание: {task[3]}\nТекст задания: {task[4]}\nКому: {Bd.get_name_by_id(task[2])}")
                    for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
                        file_s = file.split("-")
                        if file_s[0] == str(task[0]):
                            botTimeWeb.send_document(
                                message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"cr"+'\\'+file, 'rb'))
                    botTimeWeb.send_message(
                        message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Выполненые мною задания"):
        if not FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            tasks = cur.execute(
                f"Select * from tasks where to_id = '{message.chat.id}' and pass_or_not = 0;")
            tasks = list(tasks)
            botTimeWeb.send_message(
                message.chat.id, "Все ваши выполненые задания данны ниже:")
            if len(tasks) == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет выполненых заданий")
                conn.close()
            else:
                botTimeWeb.send_message(
                    message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
                for task in tasks:
                    Bd = FunkBd('userid_name')
                    botTimeWeb.send_message(
                        message.chat.id, f"Задание: {task[3]}\nТекст задания: {task[4]}\nСоздатель: {Bd.get_name_by_id(task[1])}")
                    for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
                        file_s = file.split("-")
                        if file_s[0] == str(task[0]):
                            botTimeWeb.send_document(
                                message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"cr"+'\\'+file, 'rb'))
                    conn = sqlite3.connect(
                        f'{FunkBd.cur_bd(message.chat.id)}.db')
                    cur = conn.cursor()
                    tasks_c = cur.execute(
                        f"Select * from completed_tasks where task_id = '{task[0]}'")
                    tasks_c = list(tasks_c)
                    for c_t in tasks_c:
                        botTimeWeb.send_message(
                            message.chat.id, f"⬇️Выполненое задания⬇️\nТекст выполненого задания: {c_t[1]}")
                        for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"completed"):
                            file_s = file.split("-")
                            if file_s[0] == str(task[0]):
                                botTimeWeb.send_document(
                                    message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"completed"+'\\'+file, 'rb'))
                    conn.close()
                    botTimeWeb.send_message(
                        message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Задания выполненые сотрудниками"):
        if FunkBd.cr_or_not(message.chat.id) or FunkBd.admin_or_not(message.chat.id, message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            tasks = cur.execute(
                f"Select * from tasks where from_id = '{message.chat.id}' and pass_or_not = 0;")
            tasks = list(tasks)
            botTimeWeb.send_message(
                message.chat.id, "Все ваши задания выполненые сотрудиниками данны ниже:")
            if len(tasks) == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет выполненых заданий вашими сотрудниками")
                conn.close()
            else:
                botTimeWeb.send_message(
                    message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
                for task in tasks:
                    Bd = FunkBd('userid_name')
                    botTimeWeb.send_message(
                        message.chat.id, f"Задание: {task[3]}\nТекст задания: {task[4]}\nКому: {Bd.get_name_by_id(task[2])}")
                    for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
                        file_s = file.split("-")
                        if file_s[0] == str(task[0]):
                            botTimeWeb.send_document(
                                message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"cr"+'\\'+file, 'rb'))
                    conn = sqlite3.connect(
                        f'{FunkBd.cur_bd(message.chat.id)}.db')
                    cur = conn.cursor()
                    tasks_c = cur.execute(
                        f"Select * from completed_tasks where task_id = '{task[0]}'")
                    tasks_c = list(tasks_c)
                    for c_t in tasks_c:
                        botTimeWeb.send_message(
                            message.chat.id, f"⬇️Выполненое задания⬇️\nТекст выполненого задания: {c_t[1]}")
                        for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"completed"):
                            file_s = file.split("-")
                            if file_s[0] == str(task[0]):
                                botTimeWeb.send_document(
                                    message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"completed"+'\\'+file, 'rb'))
                    conn.close()
                    botTimeWeb.send_message(
                        message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Выполнить задание"):
        if not FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            tasks = cur.execute(
                f"Select * from tasks where to_id = '{message.chat.id}' and pass_or_not = 1;")
            tasks = list(tasks)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Главное меню")
            markup.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Все ваши задания данны ниже:", reply_markup=markup)
            if len(tasks) == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данных момент у вас нет заданий")
                conn.close()
            else:
                botTimeWeb.send_message(
                    message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
                for task in tasks:
                    keyboard = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(
                        text="✅Выполнить задание✅", callback_data=f"complete_task:{task[0]}")
                    keyboard.add(button1)
                    Bd = FunkBd('userid_name')
                    botTimeWeb.send_message(
                        message.chat.id, f"Задание: {task[3]}\nТекст задания: {task[4]}\nСоздатель: {Bd.get_name_by_id(task[1])}", reply_markup=keyboard)
                    for file in os.listdir(FunkBd.cur_bd(message.from_user.id)+"cr"):
                        file_s = file.split("-")
                        if file_s[0] == str(task[0]):
                            botTimeWeb.send_document(
                                message.chat.id, open(FunkBd.cur_bd(message.from_user.id)+"cr"+'\\'+file, 'rb'))
                    botTimeWeb.send_message(
                        message.chat.id, "🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Убрать админа"):
        if FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            emp = cur.execute("Select * from users")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Главное меню")
            markup.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Уберите статус админа у сотрудника из списка ниже:", reply_markup=markup)
            count = 0
            for em in emp:
                if em[0] != str(message.chat.id) and FunkBd.admin_or_not(message.from_user.id, em[0]):
                    count += 1
                    keyboard = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(
                        text="❌Убрать статус админа❌", callback_data=f"del_admin_user:{em[0]}:{FunkBd.cur_bd(message.chat.id)}")
                    keyboard.add(button1)
                    msg = botTimeWeb.send_message(
                        message.chat.id, f"Имя: {em[1]}\nСтатус: {em[2]}\nДолжность: {em[3]}\nСсылка: https://t.me/{em[4]}", reply_markup=keyboard)
            conn.close()
            if count == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данный момент у вас нет админов")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Удалить сотрудника"):
        if FunkBd.cr_or_not(message.chat.id):
            conn = sqlite3.connect(f'{FunkBd.cur_bd(message.chat.id)}.db')
            cur = conn.cursor()
            emp = cur.execute("Select * from users")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Главное меню")
            markup.add(btn1)
            botTimeWeb.send_message(
                message.chat.id, "Удалите сотрудника из списка ниже:", reply_markup=markup)
            count = 0
            for em in emp:
                if em[0] != str(message.chat.id):
                    count += 1
                    keyboard = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(
                        text="❌Удалить сотрудника❌", callback_data=f"del_user:{em[0]}:{FunkBd.cur_bd(message.chat.id)}")
                    keyboard.add(button1)
                    msg = botTimeWeb.send_message(
                        message.chat.id, f"Имя: {em[1]}\nСтатус: {em[2]}\nДолжность: {em[3]}\nСсылка: https://t.me/{em[4]}", reply_markup=keyboard)
            conn.close()
            if count == 0:
                botTimeWeb.send_message(
                    message.chat.id, "На данный момент у вас нет сотрудников")
        else:
            botTimeWeb.send_message(
                message.chat.id, "У вас нет доступа к этой команде")
    elif (message.text == "Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую", reply_markup=markup)
    else:
        botTimeWeb.send_message(
            message.chat.id, "Sorry, I can't run this command")


def create_database(message, random_symbols):
    msg = message.text
    if msg == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую", reply_markup=markup)
    else:
        if msg == str(random_symbols):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            msg = botTimeWeb.send_message(
                message.chat.id, f"Для продолжения роботы вам требуется ввести вашу должность на этой роботе, пожалуйста введите вашу должность", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                msg, update_job_title_in_bd_create)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            random_symbols = generate_random_string(5)
            msg = botTimeWeb.send_message(
                message.chat.id, f"Код не верен,попробуйте снова. Пожалуйста введите следующие символы: {random_symbols}.", reply_markup=markup)
            botTimeWeb.register_next_step_handler(
                msg, create_database, random_symbols=random_symbols)


def switch_emp_to_BD(message):
    msg = message.text
    if msg == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            message.chat.id, text=f"{message.from_user.first_name}, пожалуйста выберете вы хотите создать новую комнату или войти уже в существующую", reply_markup=markup)
    else:
        if msg in get_names_of_database():
            conn = sqlite3.connect(f'{msg}.db')
            cur = conn.cursor()
            cur.execute("SELECT userid FROM users;")
            user_id_in_DB = cur.fetchall()
            conn.close()
            if str(message.from_user.id) not in list(map(lambda x: x[0], user_id_in_DB)):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Назад")
                markup.add(btn1)
                msg2 = botTimeWeb.send_message(
                    message.chat.id, f"Для продолжения роботы вам требуется ввести вашу должность на этой роботе, пожалуйста введите вашу должность", reply_markup=markup)
                botTimeWeb.register_next_step_handler(
                    msg2, update_job_title_in_bd_enter, db=msg)
            else:
                Bd = FunkBd('userid_name')
                if not Bd.check_execute_database_or_not(message.from_user.id, msg):
                    Bd.add_database(message.from_user.id, msg)
                Bd.set_cur_bd(message.from_user.id, msg)
                if FunkBd.cr_or_not(message.from_user.id):
                    markup = mar_creater()
                    botTimeWeb.send_message(
                        message.chat.id, text=f"Вы успешно вошли в базу данных {msg}, можете продолжать вашу роботу", reply_markup=markup)
                elif FunkBd.admin_or_not(message.from_user.id, message.from_user.id):
                    markup = mar_admin()
                    botTimeWeb.send_message(
                        message.chat.id, text=f"Вы успешно вошли в базу данных {msg}, можете продолжать вашу роботу", reply_markup=markup)
                else:
                    markup = mar_empl()
                    botTimeWeb.send_message(
                        message.chat.id, text=f"Вы успешно вошли в базу данных {msg}, можете продолжать вашу роботу", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            msg = botTimeWeb.send_message(
                message.chat.id, "Такой базы данных не существует, перепроверьте код и попробуйте снова", reply_markup=markup)
            botTimeWeb.register_next_step_handler(msg, switch_emp_to_BD)


@botTimeWeb.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split(":")
    if data[0] == "del_user":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Да", callback_data=f"del_user_yes:{data[1]}:{data[2]}")
        button2 = types.InlineKeyboardButton(
            text="Нет", callback_data=f"main_menu")
        keyboard.add(button1, button2)
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы уверенны что хотите удалить пользователя {Bd.get_name_by_id(data[1])} из базы данных {data[2]}?", reply_markup=keyboard)
    elif data[0] == "complete_task":
        msg = botTimeWeb.send_message(
            call.message.chat.id, text=f"Пожалуйста, введите текст выполненого задания")
        botTimeWeb.register_next_step_handler(
            call.message, completed_task, id_task=data[1])
    elif data[0] == "del_user_yes":
        conn = sqlite3.connect(f'{data[2]}.db')
        cur = conn.cursor()
        cur.execute(
            f"delete from users where userid = '{data[1]}'")
        conn.commit()
        conn.close()
        conn = sqlite3.connect('userid_name.db')
        cur = conn.cursor()
        cur.execute(
            f"delete from id_databases where user_id = '{data[1]}' and name_base = '{data[2]}'")
        conn.commit()
        if FunkBd.cur_bd(data[1]) == data[2]:
            cur.execute(
                f"Update user_name set cur_bd = NULL where user_id = '{data[1]}'")
            conn.commit()
        conn.close()
        markup = mar_creater()
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы успешно удалили пользователя {Bd.get_name_by_id(data[1])} из базы данных {data[2]}", reply_markup=markup)
    elif data[0] == "main_menu":
        if FunkBd.cr_or_not(call.message.chat.id):
            markup = mar_creater()
            botTimeWeb.send_message(
                call.message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        elif FunkBd.admin_or_not(call.message.chat.id, call.message.chat.id):
            markup = mar_admin()
            botTimeWeb.send_message(
                call.message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
        else:
            markup = mar_empl()
            botTimeWeb.send_message(
                call.message.chat.id, "Вы возвращены в главное меню", reply_markup=markup)
    elif data[0] == "main_menu2":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать Базу")
        btn2 = types.KeyboardButton("Войти")
        btn3 = types.KeyboardButton("Изменить мое имя")
        markup.add(btn1, btn2, btn3)
        botTimeWeb.send_message(
            call.message.chat.id, text="Вы были возвращены назад", reply_markup=markup)
    elif data[0] == "add_admin_user":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Да", callback_data=f"add_admin_user_yes:{data[1]}:{data[2]}")
        button2 = types.InlineKeyboardButton(
            text="Нет", callback_data=f"main_menu")
        keyboard.add(button1, button2)
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы уверенны что хотите добавить админом пользователя {Bd.get_name_by_id(data[1])} в базу данных {data[2]}?", reply_markup=keyboard)
    elif data[0] == "add_admin_user_yes":
        conn = sqlite3.connect(f'{data[2]}.db')
        cur = conn.cursor()
        cur.execute(
            f"update users set status = 'Admin' where userid = '{data[1]}'")
        conn.commit()
        conn.close()
        markup = mar_creater()
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы успешно добавили админом пользователя {Bd.get_name_by_id(data[1])} в базу данных {data[2]}", reply_markup=markup)
    elif data[0] == "del_admin_user":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Да", callback_data=f"del_admin_user_yes:{data[1]}:{data[2]}")
        button2 = types.InlineKeyboardButton(
            text="Нет", callback_data=f"main_menu")
        keyboard.add(button1, button2)
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы уверенны что хотите убрать статус админа у пользователя {Bd.get_name_by_id(data[1])} из базы данных {data[2]}?", reply_markup=keyboard)
    elif data[0] == "change_pers_data":
        msg = botTimeWeb.send_message(
            call.message.chat.id, "Пожалуйста введите вашу поточную должность")
        botTimeWeb.register_next_step_handler(
            msg, change_my_jt)
    elif data[0] == "add_task":
        msg = botTimeWeb.send_message(
            call.message.chat.id, "Введите название задания")
        botTimeWeb.register_next_step_handler(
            msg, create_task1, id_em=data[1])
    elif data[0] == "change_name":
        msg = botTimeWeb.send_message(
            call.message.chat.id, "Введите ваше новое полное имя (Пупкин Иван Инванович) для изменения")
        botTimeWeb.register_next_step_handler(
            msg, change_my_name)
    elif data[0] == "change_name2":
        msg = botTimeWeb.send_message(
            call.message.chat.id, "Введите ваше новое полное имя (Пупкин Иван Инванович) для изменения")
        botTimeWeb.register_next_step_handler(
            msg, change_my_name2)
    elif data[0] == "del_admin_user_yes":
        conn = sqlite3.connect(f'{data[2]}.db')
        cur = conn.cursor()
        cur.execute(
            f"update users set status = 'Employer' where userid = '{data[1]}'")
        conn.commit()
        conn.close()
        markup = mar_creater()
        Bd = FunkBd('userid_name')
        botTimeWeb.send_message(
            call.message.chat.id, f"Вы успешно убрали статус админа у пользователя {Bd.get_name_by_id(data[1])} из базы данных {data[2]}", reply_markup=markup)


FunkBd.create_basic_db()
botTimeWeb.infinity_polling()
