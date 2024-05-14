""" Contains all database methods """
import oracledb
from flask import abort
from appointment_app.qdb.config_db import host, usr, SN, pw
import traceback

class Database:
    ''' Performs actions on the database '''
    def __connect(self):
        ''' Create a connection to oracle '''
        return oracledb.connect(user=usr, password=pw, host=host,
                                service_name=SN)

    def run_file(self, file_path):
        ''' Runs an SQL script in isolation '''
        statement_parts = []
        with self.__connect() as connection:
            with connection.cursor() as cursor:
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
                                except Exception as e:
                                    print(traceback.format_exc())
                            statement_parts = []

    def get_user(self, cond):
        """ Gets a user from the database based on a condition """
        qry = f'''  SELECT user_id, is_enabled, access_level, user_type,
                    user_name, pass_word, email, avatar, phone, address,
                    age, pay_rate, specialty, warnings FROM users {cond} '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry)
                    user = cursor.fetchall()
                    if not user:
                        return None
                    return user[0]
                except Exception:
                    print(traceback.format_exc())
                    abort(500)

    def get_users(self, cond):
        """ Gets multiple users based on a condition """
        qry = f''' SELECT user_id, is_enabled, access_level, user_type,
        user_name, pass_word, email, avatar, phone, address, age, pay_rate,
        specialty FROM users {cond} '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry)
                    user = cursor.fetchall()
                    return user
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def add_user(self, user_type, user_name, pass_word, email, avatar, phone,
                 address, age, pay_rate, specialty):
        ''' Adds a user to the database '''
        qry = '''   INSERT INTO users (user_type, user_name, pass_word, email,
                    avatar, phone, address, age, pay_rate, specialty)
                    VALUES (:user_type,:user_name,:pass_word,:email,:avatar,
                    :phone,:address,:age,:pay_rate,:specialty) '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        qry, [user_type, user_name, pass_word, email, avatar,
                                phone, address, age, pay_rate, specialty])
                    connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)

    def update_user(self, user_id, user_name, email, avatar, phone, address,
                    age, pay_rate, specialty):
        ''' Updates a based on an ID '''
        query = ''' UPDATE users SET user_name = :user_name,
                    email = :email, avatar = :avatar, phone = :phone,
                    address = :address, age = :age,
                    pay_rate = :pay_rate, specialty = :specialty
                    WHERE user_id = :user_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [
                                    user_name, email, avatar, phone, address,
                                    age, pay_rate, specialty, user_id])
                    connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)

    def change_password(self, user_id, pass_word):
        ''' Changes a users password '''
        query = ''' UPDATE users SET pass_word = :pass_word
                    WHERE user_id = :user_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [pass_word, user_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def get_services(self):
        ''' function that gets all services' name '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                qry = '''   SELECT service_id, service_name, service_duration,
                            service_price, service_materials FROM services '''
                try:
                    cursor.execute(qry)
                    services = cursor.fetchall()
                    return services
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def get_service(self, cond):
        ''' function that gets a specific service' name '''
        qry = f'''  SELECT service_id, service_name, service_duration,
                    service_price, service_materials
                    FROM services {cond} '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry)
                    services = cursor.fetchall()[0]
                    return services
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def add_appointment(self, status, date_appointment, slot, venue, client_id,
                        professional_id, service_id):
        ''' Adds appointment to the database '''
        qry = '''   INSERT INTO Appointments (status, date_appointment, slot,
                    venue, client_id, professional_id, service_id)
                    VALUES (:status, :date_appointment, :slot,:venue,
                    :client_id, :professional_id,:service_id) '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(qry, [status, date_appointment, slot, venue,
                                            client_id, professional_id,
                                            service_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
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
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointments = cursor.fetchall()
                    return appointments
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def get_appointment(self, cond):
        """ Gets an appointment """
        query = f''' SELECT appointment_id, status, date_appointment, slot,
                     venue, client_id, professional_id, service_id,
                     number_services FROM appointments {cond} '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    appointment = cursor.fetchall()
                    if not appointment:
                        return None
                    return appointment[0]
                except Exception as e:
                    print(traceback.format_exc())
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
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, data_list)
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def delete_appointment(self, appointment_id):
        ''' Deletes an appointment '''
        query = ''' DELETE FROM appointments
                    WHERE appointment_id = : appointment_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [appointment_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def add_report(self, feedback_client, feedback_professional,
                   date_of_report, appointment_id):
        ''' Adds a report '''
        query = ''' INSERT INTO reports(feedback_client, feedback_professional,
                    date_of_report, appointment_id) VALUES (:feedback_client,
                    :feedback_professional, :date_of_report, :appointment_id)
                    '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query, [feedback_client, feedback_professional,
                                date_of_report, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def get_report(self, appointment_id):
        ''' Gets a report for an appointment '''
        query = ''' SELECT feedback_client, feedback_professional, report_id FROM reports
                    WHERE appointment_id = :appointment_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [appointment_id])
                    return cursor.fetchall()[0]
                except Exception as e:
                    print(traceback.format_exc())

    def delete_report(self, report_id):
        ''' Deletes a report '''
        query = ''' DELETE FROM reports
                    WHERE report_id = : report_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [report_id])
                    connection.commit()
                except oracledb.Error:
                    print(traceback.format_exc())
                    abort(500)

    def update_client_report(self, feedback_client, appointment_id):
        ''' Updates a client report '''
        query = ''' UPDATE reports SET feedback_client = : feedback_client
                    WHERE appointment_id = : appointment_id'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [feedback_client, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def update_professional_report(self, feedback_professional,
                                   appointment_id):
        ''' Updates a professional report '''
        query = ''' UPDATE reports SET
                    feedback_professional = : feedback_professional
                    WHERE appointment_id = : appointment_id'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query, [feedback_professional, appointment_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def check_if_appointment_already_has_report(self, appointment_id):
        ''' Checks if an appointment already has a report '''
        query = ''' SELECT report_id FROM reports
                    WHERE appointment_id = :appointment_id'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [appointment_id])
                    rows = cursor.fetchall()
                    return rows
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)

    def get_all_users(self):
        ''' Gets all users in the database who are not admins '''
        query = ''' SELECT user_id, is_enabled, user_type, user_name,
                    email, phone, address, age, pay_rate, specialty, warnings
                    FROM users WHERE access_level = 0'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return rows
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)
                    
    def get_all_admins(self):
        ''' Gets all users in the database who are not admins '''
        query = ''' SELECT user_id, is_enabled, user_type, user_name,
                    email, phone, address, age, pay_rate, specialty, warnings,
                    access_level FROM users WHERE access_level IN (1,2)'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return rows
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)
                        
    def delete_user(self, user_id):
        ''' Deletes a user from the database with the given user id '''
        query = ''' DELETE FROM users WHERE user_id = :user_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [user_id])
                    connection.commit()
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)
                    
    def toggle_enable_disable(self, user_id):
        # import pdb
        ''' Disables the specified user from the database '''
        get_user_query = ''' SELECT is_enabled FROM users WHERE user_id = :user_id '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(get_user_query, [user_id])
                    # pdb.set_trace()
                    is_enabled = cursor.fetchall()[0][0]
                    if is_enabled == 1:
                        disable_query = ''' UPDATE users SET is_enabled = 0 WHERE user_id = :user_id '''
                    else:
                        disable_query = ''' UPDATE users SET is_enabled = 1 WHERE user_id = :user_id '''
                    cursor.execute(disable_query, [user_id])
                    connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)

    def add_log(self, action, date_of_action, table_name, admin_name, admin_id):
        ''' Adds a log '''
        query = ''' INSERT INTO logs(action, date_of_action, table_name, admin_name,
                    admin_id) VALUES (:action,
                    :date_of_action, :table_name, :admin_name, :admin_id)
                    '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query, [action, date_of_action, table_name, admin_name, admin_id])
                    connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)
    
    def warn_user(self, user_id):
        '''warns a user'''
        query = ''' UPDATE users SET warnings = warnings + 1 WHERE user_id = :user_id'''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [user_id])
                    connection.commit()
                    check_for_3_warnings_query = '''SELECT warnings FROM users WHERE user_id = :user_id'''
                    cursor.execute(check_for_3_warnings_query, [user_id])
                    warnings = cursor.fetchall()[0][0]
                    if warnings == 3:
                        cursor.execute('UPDATE users SET is_enabled = 0, warnings= 0 WHERE user_id = :user_id', [user_id])
                        connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)   
    
    def get_logs(self, cond=None):
        """ Gets logs """
        if cond:
            query = f''' SELECT log_id, admin_id, admin_name, date_of_action, action, table_name FROM logs {cond} '''
        else:
            query = ''' SELECT log_id, admin_id, admin_name, date_of_action, action, table_name FROM logs '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    logs = cursor.fetchall()
                    return logs
                except Exception as e:
                    print(traceback.format_exc())
                    abort(500)
                    
    def add_admin(self, access_level, user_name, pass_word, email, avatar, phone, address, age):
        '''Creates an admin'''
        query = ''' INSERT INTO users (user_type, access_level, user_name, pass_word, email, avatar, phone, address, age)
                    VALUES ('Admin', :access_level, :user_name, :pass_word, :email, :avatar, :phone, :address, :age) '''
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, [access_level, user_name, pass_word, email, avatar, phone, address, age])
                    connection.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)
                    
    def toggle_access_level(self, user_id):
        '''Changes an admins access level from 1 to 2 or 2 to 1'''
        with self.__connect() as conn:
            with conn.cursor() as cursor:
                try:
                    user = self.get_user(f"WHERE user_id = {user_id}")
                    current_access_lvl = user[2]
                    if current_access_lvl == 1:
                        query = "UPDATE users SET access_level = 2 WHERE user_id = :user_id"
                    elif current_access_lvl == 2:
                        query = "UPDATE users SET access_level = 1 WHERE user_id = :user_id"
                    else:
                        return
                    cursor.execute(query, [user_id])
                    conn.commit()
                except Exception:
                    print(traceback.format_exc())
                    abort(500)
                    
    def get_appts_with_joins(self):
        query = '''
            SELECT
                    a3.appointment_id, 
                    a3.status, 
                    a3.date_appointment,         
                    a3.slot, 
                    a3.venue,
                    s.service_name,
                    u.user_name AS "Members",
                    u2.user_name AS "Professionals"
                FROM 
                    appointments a INNER JOIN services s ON a.service_id = s.service_id
                    INNER JOIN appointments a2 ON s.service_id = a2.service_id 
                    INNER JOIN users u ON a2.client_id = u.user_id
                    INNER JOIN appointments a3 ON a3.client_id = u.user_id
                    INNER JOIN users u2 ON a3.professional_id = u2.user_id; 
        '''
        
        
db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
