import mysql.connector


CREATE_TABLE = "CREATE TABLE IF NOT EXISTS \
                movie_info(\
                  cover        VARCHAR(100), \
                  name         VARCHAR(75), \
                  categroies   VARCHAR(50), \
                  pulished_at  VARCHAR(20), \
                  drama        TEXT, \
                  score        DECIMAL(10, 2), \
                  PRIMARY KEY (name, pulished_at));"


class MysqlS():
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

    
    def insert_info(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()


    def create_insert_sql(self, info_dict):
        insert_sql = f"""INSERT IGNORE INTO movie_info 
                         VALUE ("{info_dict['cover']}", 
                                "{info_dict['name']}", 
                                "{info_dict['categroies']}",
                                "{info_dict['pulished_at']}",
                                "{info_dict['drama']}", 
                                 {info_dict['score']});"""
        return insert_sql