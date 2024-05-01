'''import oracledb and its methods'''
import oracledb
from appointment_app.qdb.config_db import host, usr, sn, pw


class Database:
    ''' Performs actions on the database '''

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

    def get_user(self, cond):
        '''function to get a specific user with condition'''
        qry = f'''SELECT user_id, is_enabled, access_level, user_type, user_name, pass_word,
        email, avatar, phone, address, age, pay_rate, specialty FROM users {cond}'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry)
                    user = cursor.fetchall()[0]
                    return user
                except Exception as e:
                    print(e)

    def get_users(self, cond):
        '''function to get all users with condition'''
        qry = f'''SELECT user_id, is_enabled, access_level, user_type, user_name, pass_word,
        email, avatar, phone, address, age, pay_rate, specialty FROM users {cond}'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry)
                    user = cursor.fetchall()
                    return user
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
        '''function that update user's info'''
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
        '''function that changes the user's password'''
        query = ''' UPDATE users SET pass_word = :pass_word WHERE user_id = :user_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [pass_word, user_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_services(self):
        ''' function that gets all services' name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = "SELECT service_id, service_name, service_duration, service_price, service_materials FROM services"
                try:
                    cursor.execute(qry)
                    services = cursor.fetchall()
                    return services
                except Exception as e:
                    print(e)

    def get_service(self, cond):
        ''' function that gets a specific service' name '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                qry = f"SELECT service_id, service_name, service_duration, service_price, service_materials FROM services {
                    cond}"
                try:
                    cursor.execute(qry)
                    services = cursor.fetchall()[0]
                    return services
                except Exception as e:
                    print(e)

    def add_appointment(self, status, date_appointment, slot, venue, client_id, professional_id, service_id):
        ''' Adds appointment to the database '''
        qry = "INSERT INTO Appointments (status,date_appointment,slot,venue,client_id,professional_id,service_id) VALUES (:status,:date_appointment,:slot,:venue,:client_id,:professional_id,:service_id)"
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [
                                   status, date_appointment, slot, venue, client_id, professional_id, service_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_appointments(self, cond=None):
        '''function that gets an appointment with/without condition'''
        if cond:
            query = f''' SELECT appointment_id, status, date_appointment, slot, venue,
            client_id, professional_id, service_id, number_services FROM appointments {cond}'''
        else:
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
        '''function that gets an appointment with condition'''
        query = f''' SELECT appointment_id, status, date_appointment, slot, venue,
            client_id, professional_id, service_id, number_services FROM appointments {cond}'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointment = cursor.fetchall()[0]

                    return appointment
                except Exception as e:
                    print(e)

    def update_appointment(self, appointment_id, **kwargs):
        '''function that updates a specific appointment's info'''
        set_values = ""
        data_list = []
        for key, value in kwargs.items():
            set_values += f"{key} = :{key}, "
            data_list.append(value)
        data_list.append(appointment_id)

        set_values = set_values[:-2]  # to remove last comma + space

        query = f'''UPDATE Appointments SET {
            set_values} WHERE appointment_id = :appointment_id'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, data_list)
                    connection.commit()
                except Exception as e:
                    print(e)

    def delete_appointment(self, appointment_id):
        '''function that deletes a specific appointment through appointment_id'''
        query = ''' DELETE FROM appointments WHERE appointment_id = : appointment_id '''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def add_report(self, feedback_client, feedback_professional, date_of_report, appointment_id):
        '''function that adds a report'''
        query = 'INSERT INTO reports(feedback_client, feedback_professional, date_of_report, appointment_id) VALUES (:feedback_client, :feedback_professional, :date_of_report, :appointment_id)'
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query, [feedback_client, feedback_professional, date_of_report, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def get_report(self, appointment_id):
        '''function that gets a specific report with appointment_id'''
        query = 'SELECT feedback_client, feedback_professional FROM reports WHERE appointment_id = :appointment_id'
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    report = cursor.execute(query, [appointment_id])
                    return cursor.fetchall()[0]
                except Exception as e:
                    print(e)

    def update_client_report(self, feedback_client, appointment_id):
        '''function that updates the client's feedback'''
        query = ''' UPDATE reports SET feedback_client = : feedback_client
                    WHERE appointment_id = : appointment_id'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [feedback_client, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def update_professional_report(self, feedback_professional, appointment_id):
        '''function that updates the professional's feedback'''
        query = ''' UPDATE reports SET feedback_professional = : feedback_professional
                    WHERE appointment_id = : appointment_id'''
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query, [feedback_professional, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(e)

    def check_if_appointment_already_has_report(self, appointment_id):
        '''function that check existing report on specific appointment'''
        query = 'SELECT report_id FROM reports WHERE appointment_id = :appointment_id'
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [appointment_id])
                    rows = cursor.fetchall()
                    return rows
                except Exception as e:
                    print(e)


db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
