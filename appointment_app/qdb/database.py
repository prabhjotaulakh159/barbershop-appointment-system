import oracledb
from appointment_app.qdb.config_db import host, usr, sn, pw


class Database:
    ''' Performs actions on the database '''

    # had to re-add __init__ and __connect method to run the teacher's run_file method to update database.
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def __connect(self):
        return oracledb.connect(user=usr, password=pw, host=host,  service_name=sn)

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
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_user(self, username):
        ''' Gets a User by username '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT * FROM Users WHERE user_name = :username"
                try:
                    cursor.execute(qry, [username])
                    client = cursor.fetchall()[0]
                    return client
                except Exception as e:
                    print(e)

    def add_user(self, user_name, pass_word, professional_email, avatar, phone, rate, specialty):
        ''' Adds a professional to the database '''
        qry = "INSERT INTO Professionals (professional_name,pass_word,professional_email,avatar,phone,rate,specialty) VALUES (:professional_name,:pass_word,:professional_email,:avatar,:phone,:rate,:specialty)"
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [professional_name, pass_word,
                                         professional_email, avatar, phone, rate, specialty])
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_professional(self, professional_name):
        ''' Gets a professional by username '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT professional_id, professional_name, pass_word, professional_email, avatar, phone, rate, specialty,  FROM Professionals WHERE get_professional = :get_professional"
                try:
                    cursor.execute(qry, [professional_name])
                    professional = cursor.fetchall()[0]
                    return professional
                except Exception as e:
                    print(e)

    def get_services_name(self):
        ''' Gets all services' name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT service_name FROM Services"
                try:
                    cursor.execute(qry)
                    professional = cursor.fetchall()
                    return professional
                except Exception as e:
                    print(e)

    def get_professional_names(self):
        ''' Gets all professionals' name'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT professional_name FROM professionals"
                try:
                    cursor.execute(qry,)
                    professional = cursor.fetchall()
                    return professional
                except Exception as e:
                    print(e)

    def get_professional_id(self, professional_name):
        ''' Gets professional's id by name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT professional_id FROM professionals WHERE professional_name = :professional_name"
                try:
                    cursor.execute(qry, [professional_name])
                    professional = cursor.fetchall()[0]
                    return professional
                except Exception as e:
                    print(e)

    def get_service_id(self, service_name):
        ''' Gets service's id by name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT service_id FROM services WHERE service_name = :service_name"
                try:
                    cursor.execute(qry, [service_name])
                    professional = cursor.fetchall()[0]
                    return professional
                except Exception as e:
                    print(e)

    def add_appointment(self, status, date_appointment, slot, venue, client_id, prof_id, service_id):
        ''' Adds appointment to the database '''
        qry = "INSERT INTO Appointments (status,date_appointment,slot,venue,client_id,prof_id,service_id) VALUES (:status,:date_appointment,:slot,:venue,:client_id,:prof_id,:service_id)"
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [status, date_appointment,
                                         slot, venue, client_id, prof_id, service_id])
                    connection.commit()
                except Exception as e:
                    print(e)


db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
