# coding: utf-8

import sqlite3
import asyncio
import json
from freebox_api import Freepybox
from datetime import datetime

# from freebox_api.aiofreepybox import DEFAULT_TOKEN_FILE

display_json=False

def db_get_last_host_state(cursor,primary_name):
    sql = "SELECT * from devices where primary_name='" + str(primary_name) + "' ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    rows = cursor.fetchall()

    if not len(rows):
        #new host
        return False
    else:
        row = rows[-1]
        return (row[0],row[8])

def db_insert_new_host_value(cursor,id,primary_name,host_type,first_activity,last_activity,last_time_reachable,value):
    current_datetime = int(datetime.timestamp(datetime.now()))
    datas = (current_datetime, id, primary_name, host_type, first_activity, last_activity, last_time_reachable, value)
    sql = "INSERT INTO devices(timestamp, device_id, primary_name, host_type, first_activity, last_activity, last_time_reachable, value) VALUES" + str(
        datas)
    cursor.execute(sql)

def db_update_host_value(cursor,host_id,last_activity,last_time_reachable):
    current_datetime = int(datetime.timestamp(datetime.now()))
    sql = ("UPDATE devices SET timestamp='" + str(current_datetime)
           + "', last_activity='" + str(last_activity)
           + "', last_time_reachable='" + str(last_time_reachable)
           + "' " + "WHERE id=" + str(host_id))
    cursor.execute(sql)

def db_add_data(cursor,id,primary_name,host_type,first_activity,last_activity,last_time_reachable,value):
    ret = db_get_last_host_state(cursor,primary_name)
    if not ret:
        db_insert_new_host_value(cursor, id, primary_name, host_type, first_activity, last_activity,
                                 last_time_reachable, value)
    else :
        host_id,state = ret
        if(state != value):
            db_insert_new_host_value(cursor, id, primary_name, host_type, first_activity, last_activity,
                                     last_time_reachable, value)
        else :
            db_update_host_value(cursor,host_id, last_activity, last_time_reachable)






async def demo():
    # Instantiate Freepybox class using default application descriptor
    # and default token_file location
    fbx = Freepybox(api_version="latest")
    await fbx.open(host="mafreebox.freebox.fr", port=443)

    ##############
    # Connection #
    ##############

    conn_config = await fbx.connection.get_config()
    print(
        f"Freebox API access : https://{conn_config['api_domain']}:{conn_config['https_port']}/"
    )

    conn = sqlite3.connect('hosts.db')

    cursor = conn.cursor()
    cursor.execute("""
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
    conn.commit()

    ##############
    # LAN        #
    ##############

    fbx_lan_hosts = await fbx.lan.get_hosts_list()

    #host active
    print("hosts_actives :")
    for h in fbx_lan_hosts:
        if h['active']:
            db_add_data(cursor, h['id'], h['primary_name'], h['host_type'], h['first_activity'], h['last_activity'],
                     h['last_time_reachable'],1)
        else :
            db_add_data(cursor, h['id'], h['primary_name'], h['host_type'], h['first_activity'], h['last_activity'],
                     h['last_time_reachable'],0)
    conn.commit()

    if display_json :
        #display all
        for h in fbx_lan_hosts:
            print(json.dumps(h, sort_keys=True, indent=4))

    # Close the Freebox session
    await fbx.close()
    print("=" * 50)
    print("= Disconnected =")
    print("=" * 50)
    print("\n" * 2)

    conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()
