from functiontg import *


class FunkBd:
    def __init__(self, name_database):
        self.name_database = name_database

    @staticmethod
    def create_basic_db():
        conn = sqlite3.connect('userid_name.db')
        cur = conn.cursor()
        cur.execute(
            "Create table IF NOT EXISTS user_name(user_id TEXT PRIMARY KEY, name TEXT, cur_bd TEXT);")
        cur.execute(
            "create table IF NOT EXISTS id_databases(user_id TEXT,name_base TEXT);")
        conn.commit()
        conn.close()

    def check_job_title_id_in_bd(self, id):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        job_title = cur.execute(
            f"Select job_title from users where userid = '{id}'")
        job_title = list(job_title)
        conn.close()
        return '-' == job_title[0][0]

    def add_database(self, id, database):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute(
            f"Insert into id_databases values('{id}','{database}')")
        conn.commit()
        conn.close()

    def check_execute_database_or_not(self, id, database):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        databases_of_user = cur.execute(
            f"Select name_base from id_databases where user_id = '{id}'")
        databases_of_user = databases_of_user.fetchall()
        databases_of_user = list(map(lambda x: x[0], databases_of_user))
        conn.close()
        return str(database) in databases_of_user

    @staticmethod
    def cur_bd(id):
        conn = sqlite3.connect('userid_name.db')
        cur = conn.cursor()
        cur.execute(f"SELECT cur_bd FROM user_name where user_id = '{id}';")
        user_cur_bd = cur.fetchone()
        conn.close()
        return user_cur_bd[0]

    @staticmethod
    def cr_or_not(id):
        Bd = FunkBd('userid_name')
        conn = sqlite3.connect(f'{Bd.cur_bd(id)}.db')
        cur = conn.cursor()
        cr_or_not = cur.execute(
            f"Select userid from users where status  = 'Creater'")
        cr_or_not = cr_or_not.fetchall()
        cr_or_not = list(map(lambda x: x[0], cr_or_not))
        conn.close()
        return str(id) in cr_or_not

    @staticmethod
    def check_info_id_in_bd(id, base):
        conn = sqlite3.connect(f'{base}.db')
        cur = conn.cursor()
        info = cur.execute(f"Select userid from users where userid = '{id}';")
        return len(list(info)) == 1

    @staticmethod
    def admin_or_not(message_id, id):
        Bd = FunkBd('userid_name')
        conn = sqlite3.connect(f'{Bd.cur_bd(message_id)}.db')
        cur = conn.cursor()
        ad_or_not = cur.execute(
            f"Select userid from users where status = 'Admin'")
        ad_or_not = ad_or_not.fetchall()
        ad_or_not = list(map(lambda x: x[0], ad_or_not))
        conn.close()
        return str(id) in ad_or_not

    def set_cur_bd(self, id, text):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        conn.execute(
            f"update user_name set cur_bd = '{text}' where user_id = '{id}'")
        conn.commit()
        conn.close()

    def add_new_user(self, message):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute(
            f"INSERT into user_name values({message.from_user.id}, '{message.text}', NULL);")
        conn.commit()
        conn.close()

    def get_id_of_users(self):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM user_name;")
        user_id_in_DB = cur.fetchall()
        conn.close()
        return list(map(lambda x: x[0], user_id_in_DB))

    def get_name_by_id(self, id):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute(f"SELECT name FROM user_name where user_id = '{id}';")
        user_id_in_DB = cur.fetchone()
        conn.close()
        return user_id_in_DB[0]

    def update_personal_data(self, message, name, job_title):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute(
            f"Update user_name set name = '{name}', job_title = '{job_title}' where user_id = '{message.chat.id}';")
        conn.commit()
        conn.close()

    def get_job_title_by_id(self, id):
        conn = sqlite3.connect(f'{self.name_database}.db')
        cur = conn.cursor()
        cur.execute(f"SELECT job_title FROM user_name where user_id = '{id}';")
        user_id_in_DB = cur.fetchone()
        conn.close()
        return user_id_in_DB[0]
