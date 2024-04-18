import os
import oracledb

from project.qdb.config_db import host, usr, sn, pw


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
            
#-----------------------------------------------------------




#-----------------------------------------------------------
db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
    db.close()

