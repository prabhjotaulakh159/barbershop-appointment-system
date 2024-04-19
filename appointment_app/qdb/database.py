import os
import oracledb

from appointment_app.qdb.config_db import host, usr, sn, pw


class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def __connect(self):
        return oracledb.connect(user=usr, password=pw, host=host,  service_name=sn)

    def db_conn(self):
        return self.__connection

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            # pdb.set_trace()
            with open(file_path, 'r') as f:
                for line in f:
                    if line[:2] == '--':
                        continue
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                # pdb.set_trace()
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []

    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def get_cursor(self):
        for i in range(3):
            try:
                return self.__connection.cursor()
            except Exception:
                # Might need to reconnect
                self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()

    def run_sql_script(self, sql_filename):
        if os.path.exists(sql_filename):
            self.__connect()
            self.__run_file(sql_filename)
            self.close()
        else:
            print('Invalid Path')

# -----------------------------------------------------------
    def add_client(self, user_name, pass_word, email, avatar, phone):
        qry = "INSERT INTO Clients (user_name,pass_word,email,avatar,phone) VALUES (:user_name,:pass_word,:email,:avatar,:phone)"
        with self.__connection.cursor() as cur:
            try:
                res = cur.execute(
                    qry, (user_name, pass_word, email, avatar, phone))
            except Exception as e:
                print(e)

    def get_client(self, username):
        with self.__connection.cursor() as cur:
            qry = f"SELECT * FROM Clients WHERE user_name = '{username}'"
            try:
                r = cur.execute(qry).fetchone()
                return r
            except Exception as e:
                print(e)

    def add_professional(self, prof_name, pass_word, prof_email, avatar, phone, rate, specialty):
        qry = "INSERT INTO Professionals (prof_name,pass_word,prof_email,avatar,phone,rate,specialty) VALUES (:prof_name,:pass_word,:prof_email,:avatar,:phone,:rate,:specialty)"
        with self.__connection.cursor() as cur:
            try:
                res = cur.execute(qry, (prof_name, pass_word,
                                  prof_email, avatar, phone, rate, specialty))
            except Exception as e:
                print(e)
                
    def get_professional(self, prof_name):
        with self.__connection.cursor() as cur:
            qry = f"SELECT * FROM Professionals WHERE prof_name = '{prof_name}'"
            try:
                r = cur.execute(qry).fetchone()
                return r
            except Exception as e:
                print(e)

# -----------------------------------------------------------
db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
    db.close()
