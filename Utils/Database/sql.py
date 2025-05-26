import mysql.connector
import datetime

class Database:
    def __init__(kimin):
        kimin.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Udin@100901",
            database="jarvis"
        )
        
        kimin.cursor = kimin.db.cursor(dictionary=True)

    def Get_Time(kimin, format="%Y-%m-%d"):
        now = datetime.datetime.now()
        now = now.strftime(format)
        return now

    def Get_Data(kimin, nama_tabel):
        kimin.cursor.execute(f"SELECT * FROM {nama_tabel}")
        data = kimin.cursor.fetchall()
        hasil = {}
        hasil['total_data'] = len(data)
        hasil['data'] = data
        return hasil
    
    def Add_Data(kimin, **parameter):
        kolom = ", ".join(parameter['data'].keys())
        value_placeholder = ", ".join(['%s'] * len(parameter['data']))
        
        query = f"INSERT INTO {parameter['tabel']} ({kolom}) VALUES ({value_placeholder})"
        
        # Ambil data sebagai tuple untuk parameterized query
        values = tuple(parameter['data'].values())
        kimin.cursor.execute(query, values)
        kimin.db.commit()

    def ExecuteSQL(kimin, **parameter):
        hasil = {'status': False}
        try:
            hasil['query'] = parameter['query']
            kimin.cursor.execute(parameter['query'])
            hasil['result'] = kimin.cursor.fetchall()
            hasil['status'] = True
        except Exception as e:
            hasil['error'] = e
        return hasil
