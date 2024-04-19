import oracledb
from appointment_app.qdb.config_db import host, usr, sn, pw


class Database:
    def connect(self):
        return oracledb.connect(user=usr, password=pw, host=host,
                                service_name=sn)

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


db = Database()

if __name__ == '__main__':
    db.run_file('database.sql')
