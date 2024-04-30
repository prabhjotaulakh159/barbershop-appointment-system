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

    def get_user_with_id(self, user_id):
        ''' Gets a user by user id '''
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
                        user_id = :user_id 
                    '''
                try:
                    cursor.execute(qry, [user_id])
                    user = cursor.fetchall()[0]
                    return user
                except Exception as e:
                    print(e)

    def get_member_names(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = ''' 
                    SELECT user_name FROM users WHERE user_type = 'Member'  
                    '''
                try:
                    cursor.execute(qry)
                    members = cursor.fetchall()
                    return members
                except Exception as e:
                    print(e)

    def add_user(self, user_type, user_name, pass_word, email, avatar, phone, address, age, pay_rate, specialty):
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

    def update_user(self, user_id, user_name, email, avatar, phone, address, age, pay_rate, specialty):
        query = ''' UPDATE users SET user_name = :user_name,
                    email = :email, avatar = :avatar, phone = :phone, address = :address, age = :age,
                    pay_rate = :pay_rate, specialty = :specialty
                    WHERE user_id = :user_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [
                                   user_name, email, avatar, phone, address, age, pay_rate, specialty, user_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def change_password(self, user_id, pass_word):
        query = ''' UPDATE users SET pass_word = :pass_word WHERE user_id = :user_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [pass_word, user_id])
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

    def get_service_name(self, service_id):
        ''' Gets all services' name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT service_name FROM Services WHERE service_id = :service_id"
                try:
                    cursor.execute(qry, [service_id])
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

    def get_user_id(self, cond):
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

    def get_appointment(self, cond):
        query = f''' SELECT appointment_id, status, date_appointment, slot, venue,
            client_id, professional_id, service_id, number_services FROM appointments WHERE {cond}'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointment = cursor.fetchall()[0]

                    return appointment
                except Exception as e:
                    print(e)

    def get_my_appointments(self, cond):
        query = f''' SELECT appointment_id, status, date_appointment, slot, venue,
            client_id, professional_id, service_id, number_services FROM appointments WHERE {cond}'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointments = cursor.fetchall()
                    return appointments
                except Exception as e:
                    print(e)

    def update_appointment(self, appointment_id, date_appointment, slot, venue, service_id):
        query = ''' UPDATE Appointments SET date_appointment = :date_appointment,
                    slot = :slot, venue = :venue, service_id = :service_id
                    WHERE appointment_id = :appointment_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [
                        date_appointment, slot, venue, service_id, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def update_appointment_admin(self, appointment_id, date_appointment, slot, venue, client_id, professional_id, service_id):
        query = ''' UPDATE Appointments SET date_appointment = :date_appointment,
                    slot = :slot, venue = :venue, client_id = :client_id, professional_id = :professional_id, service_id = :service_id
                    WHERE appointment_id = :appointment_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [
                        date_appointment, slot, venue, client_id, professional_id, service_id, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)


db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
