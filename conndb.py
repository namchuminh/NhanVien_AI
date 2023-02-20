import mysql.connector

class conndb:
    def __init__(self):
        pass
    
    def queryResult(self, strsql):
        cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='nhanvien_ai')
        conn = cnx.cursor()
        conn.execute(strsql)
        result = conn.fetchall()
        return result
    
    def queryExecute(self, strsql):
        cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='nhanvien_ai')
        conn = cnx.cursor()
        conn.execute(strsql)
        cnx.commit()
