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
                        
    def get_user(self, username):
        ''' Gets a user by username '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = ''' 
                    SELECT 
                        user_id,
                        is_enabled,
                        access_level,
                        user_type, 
                        user_name,
                        pass_word,
                        email,
                        avatar,
                        phone,
                        address,
                        age,
                        pay_rate,
                        specialty
                    FROM 
                        users 
                    WHERE
                        user_name = :username 
                    '''
                try:
                    cursor.execute(qry, [username])
                    user = cursor.fetchall()[0]
                    return user
                except Exception as e:
                    print(e)

    def add_user(self, user_type, user_name ,pass_word, email, avatar, phone, address, age, pay_rate, specialty):
        ''' Adds a user to the database '''
        qry = "INSERT INTO users (user_type,user_name,pass_word,email,avatar,phone,address,age,pay_rate,specialty) VALUES (:user_type,:user_name,:pass_word,:email,:avatar,:phone,:address,:age,:pay_rate,:specialty)"
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        qry, [user_type, user_name, pass_word, email, avatar, phone, address, age, pay_rate, specialty])
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_services_name(self):
        ''' Gets all services' name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT service_name FROM Services"
                try:
                    cursor.execute(qry)
                    services = cursor.fetchall()
                    return services
                except Exception as e:
                    print(e)

    def get_professional_names(self):
        ''' Gets all professionals' name'''
        with self.connect() as connection:
            with connection.cursor() as cursor: 
                qry = "SELECT user_name FROM Users WHERE user_type = 'Professional'"
                try:
                    cursor.execute(qry)
                    professional = cursor.fetchall()
                    return professional
                except Exception as e:
                    print(e)

    def get_user_id(self,cond):
        ''' Gets professional's id by name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = f"SELECT user_id FROM Users WHERE {cond}"
                print(qry)
                try:
                    cursor.execute(qry)
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

    def add_appointment(self, status, date_appointment, slot, venue, client_id, professional_id, service_id):
        ''' Adds appointment to the database '''
        qry = "INSERT INTO Appointments (status,date_appointment,slot,venue,client_id,professional_id,service_id) VALUES (:status,:date_appointment,:slot,:venue,:client_id,:professional_id,:service_id)"
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [status, date_appointment,
                                         slot, venue, client_id, professional_id, service_id])
                    connection.commit()
                except Exception as e:
                    print(e)
                    
    def get_appointments(self):
        query = ''' SELECT appointment_id, status, date_appointment, slot, venue,
            client_id, professional_id, service_id, number_services FROM appointments'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointments = cursor.fetchall()
                    return appointments
                except Exception as e:
                    print(e)

db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
