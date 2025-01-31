import sqlite3
from datetime import datetime

cDevices_uid=0
cDevices_timestamp=1
cDevices_device_id=2
cDevices_primary_name=3
cDevices_host_type=4
cDevices_first_activity=5
cDevices_last_activity=6
cDevices_last_time_reachable=7
cDevices_values=8

cValue_active=1
cValue_inactive=0

class Database:
    def __init__(self, path='hosts.db'):
        self.path=path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.create()

    def get_last_host_state(self,primary_name):
        sql = "SELECT * from devices where primary_name='" + str(primary_name) + "' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if not len(rows):
            #new host
            return False
        else:
            row = rows[-1]
            return (row[0],row[8])

    def insert_new_host_value(self,id,primary_name,host_type,first_activity,last_activity,last_time_reachable,value):
        current_datetime = int(datetime.timestamp(datetime.now()))
        datas = (current_datetime, id, primary_name, host_type, first_activity, last_activity, last_time_reachable, value)
        sql = "INSERT INTO devices(timestamp, device_id, primary_name, host_type, first_activity, last_activity, last_time_reachable, value) VALUES" + str(
            datas)
        self.cursor.execute(sql)

    def update_host_value(self,host_id,last_activity,last_time_reachable):
        current_datetime = int(datetime.timestamp(datetime.now()))
        sql = ("UPDATE devices SET timestamp='" + str(current_datetime)
               + "', last_activity='" + str(last_activity)
               + "', last_time_reachable='" + str(last_time_reachable)
               + "' " + "WHERE id=" + str(host_id))
        self.cursor.execute(sql)

    def add_data(self,device_id,primary_name,host_type,first_activity,last_activity,last_time_reachable,value):
        ret = self.get_last_host_state(primary_name)
        if not ret:
            self.insert_new_host_value(device_id, primary_name, host_type, first_activity, last_activity,
                                     last_time_reachable, value)
        else :
            host_id,state = ret
            if state != value:
                self.insert_new_host_value(device_id, primary_name, host_type, first_activity, last_activity,
                                         last_time_reachable, value)
            else :
                self.update_host_value(host_id, last_activity, last_time_reachable)

    def get_hosts(self):
        sql = "SELECT DISTINCT primary_name FROM devices"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_host_data(self, host):
        sql = 'SELECT * FROM devices where primary_name is "' + host+'"'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def create(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             timestamp INTERGER,
             device_id TEXT,
             primary_name TEXT,
             host_type TEXT,
             first_activity INTERGER,
             last_activity INTERGER,
             last_time_reachable INTERGER,
             value INTERGER
        )
        """)
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()