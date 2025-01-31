# coding: utf-8
import asyncio
import json
from freebox_api import Freepybox
from database import *

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

    db=Database()

    ##############
    # LAN        #
    ##############
    fbx_lan_hosts = await fbx.lan.get_hosts_list()

    #host active
    print("hosts_actives :")
    for h in fbx_lan_hosts:
        if h['active']:
            db.add_data(h['id'], h['primary_name'], h['host_type'], h['first_activity'], h['last_activity'],
                     h['last_time_reachable'],1)
        else :
            db.add_data(h['id'], h['primary_name'], h['host_type'], h['first_activity'], h['last_activity'],
                     h['last_time_reachable'],0)
    db.commit()


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

    db.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(demo())
loop.close()
