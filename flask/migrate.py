from logging import addLevelName

from database import *

if __name__ == '__main__':
    db_src = Database('src.db')
    db_dst = Database('new.db')
    lines = db_src.get_all_data()
    db_src.close()

    time=1738075800
    dico_devices = {}
    for line in lines:
        try :
            hostname=line[cDevices_primary_name]
            time=int(line[cDevices_timestamp])
            date=datetime.fromtimestamp(time)
            uid=line[cDevices_uid]
            if dico_devices[hostname]:
                ecart=time-int(dico_devices[line[cDevices_primary_name]])
                dico_devices[hostname]=time

                if ecart > 1000:
                    db_dst.add_data(line[cDevices_device_id],
                                    line[cDevices_primary_name],
                                    line[cDevices_host_type],
                                    line[cDevices_first_activity],
                                    line[cDevices_last_activity],
                                    line[cDevices_last_time_reachable],
                                    cValue_inactive,int(line[cDevices_timestamp])-1)
                else:
                    db_dst.add_data(line[cDevices_device_id],
                                    line[cDevices_primary_name],
                                    line[cDevices_host_type],
                                    line[cDevices_first_activity],
                                    line[cDevices_last_activity],
                                    line[cDevices_last_time_reachable],
                                    cValue_active,int(line[cDevices_timestamp])-1)
                db_dst.commit()
        except :
            dico_devices[line[cDevices_primary_name]] = int(line[cDevices_timestamp])
    db_dst.close()
