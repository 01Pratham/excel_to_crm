import mysql.connector as mysql

host = "localhost"
username = "idxesdsd_cal"
password = "v2BFvmbge2P+#C"
databaseName = 'idxesdsd_cal_v2'

Connection = mysql.connect(host=host, user=username, password=password, database=databaseName)

if Connection.is_connected():
    print("Connected")
    cursor = Connection.cursor()
    cursor = Connection.cursor(dictionary=True)

