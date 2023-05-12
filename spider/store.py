import mysql.connector


CREATE_TABLE = "CREATE TABLE IF NOT EXISTS \
                movie_info(\
                  cover        VARCHAR(100), \
                  name         VARCHAR(75), \
                  categroies   VARCHAR(50), \
                  pulished_at  VARCHAR(20), \
                  drama        TEXT, \
                  score        DECIMAL(10, 2));"


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


    def create_insert_sql(self, cover, name, categroies, pulished_at, drama, score):
        insert_sql = f"""INSERT IGNORE INTO movie_info 
                         VALUE ("{cover}", 
                                "{name}", 
                                "{categroies}",
                                "{pulished_at}",
                                "{drama}", 
                                 {score});"""
        return insert_sql