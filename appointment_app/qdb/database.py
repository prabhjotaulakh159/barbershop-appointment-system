""" Contains all database methods """
import oracledb
from flask import abort
from appointment_app.qdb.config_db import host, usr, SN, pw


class Database:
    ''' Performs actions on the database '''
    
    def __init__(self):
        self.connection = self.__connect()

    def __connect(self):
        ''' Create a connection to oracle '''
        return oracledb.connect(user=usr, password=pw, host=host,
                                service_name=SN)

    def run_file(self, file_path):
        ''' Runs an SQL script in isolation '''
        statement_parts = []
        with self.connection.cursor() as cursor:
            with open(file_path, 'r', encoding='UTF-8') as f:
                for line in f:
                    if line[:2] == '--':
                        continue
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except oracledb.Error as e:
                                print(e)
                        statement_parts = []

    def get_user(self, cond):
        """ Gets a user from the database based on a condition """
        qry = f'''  SELECT user_id, is_enabled, access_level, user_type,
                    user_name, pass_word, email, avatar, phone, address,
                    age, pay_rate, specialty FROM users {cond} '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(qry)
                user = cursor.fetchall()[0]
                return user
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_users(self, cond):
        """ Gets multiple users based on a condition """
        qry = f''' SELECT user_id, is_enabled, access_level, user_type,
        user_name, pass_word, email, avatar, phone, address, age, pay_rate,
        specialty FROM users {cond} '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(qry)
                user = cursor.fetchall()
                return user
            except oracledb.Error as e:
                print(e)
                abort(500)

    def add_user(self, user_type, user_name, pass_word, email, avatar, phone,
                 address, age, pay_rate, specialty):
        ''' Adds a user to the database '''
        qry = '''   INSERT INTO users (user_type, user_name, pass_word, email,
                    avatar, phone, address, age, pay_rate, specialty)
                    VALUES (:user_type,:user_name,:pass_word,:email,:avatar,
                    :phone,:address,:age,:pay_rate,:specialty) '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    qry, [user_type, user_name, pass_word, email, avatar,
                            phone, address, age, pay_rate, specialty])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def update_user(self, user_id, user_name, email, avatar, phone, address,
                    age, pay_rate, specialty):
        ''' Updates a based on an ID '''
        query = ''' UPDATE users SET user_name = :user_name,
                    email = :email, avatar = :avatar, phone = :phone,
                    address = :address, age = :age,
                    pay_rate = :pay_rate, specialty = :specialty
                    WHERE user_id = :user_id '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [
                                user_name, email, avatar, phone, address,
                                age, pay_rate, specialty, user_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def change_password(self, user_id, pass_word):
        ''' Changes a users password '''
        query = ''' UPDATE users SET pass_word = :pass_word
                    WHERE user_id = :user_id '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [pass_word, user_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_services(self):
        ''' function that gets all services' name '''
        with self.connection.cursor() as cursor:
            qry = '''   SELECT service_id, service_name, service_duration,
                        service_price, service_materials FROM services '''
            try:
                cursor.execute(qry)
                services = cursor.fetchall()
                return services
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_service(self, cond):
        ''' function that gets a specific service' name '''
        qry = f'''  SELECT service_id, service_name, service_duration,
                    service_price, service_materials
                    FROM services {cond} '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(qry)
                services = cursor.fetchall()[0]
                return services
            except oracledb.Error as e:
                print(e)
                abort(500)

    def add_appointment(self, status, date_appointment, slot, venue, client_id,
                        professional_id, service_id):
        ''' Adds appointment to the database '''
        qry = '''   INSERT INTO Appointments (status, date_appointment, slot,
                    venue, client_id, professional_id, service_id)
                    VALUES (:status, :date_appointment, :slot,:venue,
                    :client_id, :professional_id,:service_id) '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(qry, [status, date_appointment, slot, venue,
                                        client_id, professional_id,
                                        service_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_appointments(self, cond=None):
        """ Gets appointments """
        if cond:
            query = f''' SELECT appointment_id, status, date_appointment,
                         slot, venue, client_id, professional_id, service_id,
                         number_services FROM appointments {cond} '''
        else:
            query = ''' SELECT appointment_id, status, date_appointment, slot,
            venue, client_id, professional_id, service_id, number_services
            FROM appointments '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                appointments = cursor.fetchall()
                return appointments
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_appointment(self, cond):
        """ Gets an appointment """
        query = f''' SELECT appointment_id, status, date_appointment, slot,
                     venue, client_id, professional_id, service_id,
                     number_services FROM appointments {cond} '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                appointment = cursor.fetchall()[0]
                return appointment
            except oracledb.Error as e:
                print(e)
                abort(500)

    def update_appointment(self, appointment_id, **kwargs):
        """ Updates an appointment """
        set_values = ""
        data_list = []
        for key, value in kwargs.items():
            set_values += f"{key} = :{key}, "
            data_list.append(value)
        data_list.append(appointment_id)

        set_values = set_values[:-2]  # to remove last comma + space

        query = f'''UPDATE Appointments SET {
            set_values} WHERE appointment_id = :appointment_id'''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data_list)
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def delete_appointment(self, appointment_id):
        ''' Deletes an appointment '''
        query = ''' DELETE FROM appointments
                    WHERE appointment_id = : appointment_id '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [appointment_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def add_report(self, feedback_client, feedback_professional,
                   date_of_report, appointment_id):
        ''' Adds a report '''
        query = ''' INSERT INTO reports(feedback_client, feedback_professional,
                    date_of_report, appointment_id) VALUES (:feedback_client,
                    :feedback_professional, :date_of_report, :appointment_id)
                    '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    query, [feedback_client, feedback_professional,
                            date_of_report, appointment_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_report(self, appointment_id):
        ''' Gets a report for an appointment '''
        query = ''' SELECT feedback_client, feedback_professional FROM reports
                    WHERE appointment_id = :appointment_id '''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [appointment_id])
                return cursor.fetchall()[0]
            except oracledb.Error as e:
                print(e)
                abort(500)

    def update_client_report(self, feedback_client, appointment_id):
        ''' Updates a client report '''
        query = ''' UPDATE reports SET feedback_client = : feedback_client
                    WHERE appointment_id = : appointment_id'''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [feedback_client, appointment_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def update_professional_report(self, feedback_professional,
                                   appointment_id):
        ''' Updates a professional report '''
        query = ''' UPDATE reports SET
                    feedback_professional = : feedback_professional
                    WHERE appointment_id = : appointment_id'''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    query, [feedback_professional, appointment_id])
                self.connection.commit()
            except oracledb.Error as e:
                print(e)
                abort(500)

    def check_if_appointment_already_has_report(self, appointment_id):
        ''' Checks if an appointment already has a report '''
        query = ''' SELECT report_id FROM reports
                    WHERE appointment_id = :appointment_id'''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, [appointment_id])
                rows = cursor.fetchall()
                return rows
            except oracledb.Error as e:
                print(e)
                abort(500)

    def get_all_users(self):
        ''' Gets all users in the database who are not admins '''
        query = ''' SELECT user_id, is_enabled, user_type, user_name,
                    email, phone, address, age, pay_rate, specialty
                    FROM users WHERE access_level = 0'''
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
            except oracledb.Error as e:
                print(e)
                abort(500)


db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
