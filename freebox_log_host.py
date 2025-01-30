# coding: utf-8

import sqlite3
import asyncio
import json
from freebox_api import Freepybox
from datetime import datetime

# from freebox_api.aiofreepybox import DEFAULT_TOKEN_FILE

display_json=False

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
         last_time_reachable INTERGER
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
            current_datetime = int(datetime.timestamp(datetime.now()))
            datas = (current_datetime,h['id'],h['primary_name'],h['host_type'],h['first_activity'],h['last_activity'],h['last_time_reachable'])
            sql="INSERT INTO devices(timestamp, device_id, primary_name, host_type, first_activity, last_activity, last_time_reachable) VALUES"+str(datas)
            print(datas)
            cursor.execute(sql)
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
