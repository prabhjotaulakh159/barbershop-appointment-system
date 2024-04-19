import oracledb
from appointment_app.qdb.config_db import host, usr, sn, pw


class Database:
    ''' Performs actions on the database '''
    def connect(self):
        ''' Create a connection to oracle '''
        return oracledb.connect(user=usr, password=pw, host=host,
                                service_name=sn)

    def run_file(self, file_path):
        ''' Runs an SQL script in isolation '''
        statement_parts = []
        with self.__connection.cursor() as cursor:
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

    def add_client(self, user_name, pass_word, email, avatar, phone):
        ''' Adds a client to the database '''
        qry = '''
            INSERT INTO clients (user_name, pass_word, email,
            avatar, phone) VALUES
            (:user_name, :pass_word, :email,: avatar, :phone)
        '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [user_name, pass_word, email, avatar,
                                         phone])
                except Exception as e:
                    print(e)

    def get_client(self, username):
        ''' Gets a client by username '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT client_id, user_name, pass_word, email, avatar, phone FROM Clients WHERE user_name = :username"
                try:
                    cursor.execute(qry, [username])
                    client = cursor.fetchall()
                    return client
                except Exception as e:
                    print(e)

    def add_professional(self, prof_name, pass_word, prof_email, avatar, phone, rate, specialty):
        qry = "INSERT INTO Professionals (prof_name,pass_word,prof_email,avatar,phone,rate,specialty) VALUES (:prof_name,:pass_word,:prof_email,:avatar,:phone,:rate,:specialty)"
        with self.connect() as cur:
            try:
                res = cur.execute(qry, (prof_name, pass_word,
                                  prof_email, avatar, phone, rate, specialty))
            except Exception as e:
                print(e)
                
    def get_professional(self, prof_name):
        with self.connect() as cur:
            qry = f"SELECT * FROM Professionals WHERE prof_name = '{prof_name}'"
            try:
                r = cur.execute(qry).fetchone()
                return r
            except Exception as e:
                print(e)
db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
