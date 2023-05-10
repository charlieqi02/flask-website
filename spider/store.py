import mysql.connector


CREATE_TABLE = "CREATE TABLE IF NOT EXISTS \
                personal_info(\
                  name      VARCHAR(255), \
                  gender    VARCHAR(255), \
                  age       INT, \
                  PRIMARY KEY (name, gender, age));"

INSERT_INFO = 'INSERT IGNORE INTO personal_info VALUE ("{name}","{gender}",{age})'


class Mysql():
    def __init__(self):
        # connect to mysql
        self.conn = mysql.connector.connect(user = "root",
                                            password = "1q2w3e4r",
                                            host = "localhost",
                                            database = 'flask_website',
                                            auth_plugin = 'mysql_native_password')
        

    def create_table(self, sql=CREATE_TABLE):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    
    def insert_info(self, sql=INSERT_INFO):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.commit()
        cursor.close()