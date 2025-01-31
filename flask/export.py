import sqlite3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from database import *


def generate_graph(path,plt,host,offset,from_time,to_time):
    #display only if host is active during selected time range
    display = False
    db = Database(path)
    rows = db.get_host_data(host)
    # print(rows)
    db.close()
    last_activity = []
    values = []
    # first xy
    last_activity.append(datetime.fromtimestamp(from_time))
    values.append(rows[0][cDevices_values]+offset)
    # print(datetime.fromtimestamp(from_time),rows[0][cDevices_values])
    for row in rows:
        state=row[cDevices_values]
        timestamp=int(row[cDevices_timestamp])
        # if values[-1] == state + offset :
        #     #last elements is the same as new one
        #     last_activity.append(datetime.fromtimestamp(timestamp))
        #     values.append(state + offset)
        #     print(datetime.fromtimestamp(from_time), rows[0][cDevices_values])
        # else :
        if state == cValue_active :
            last_activity.append(datetime.fromtimestamp(timestamp - 1))
            values.append(cValue_active + offset)
            last_activity.append(datetime.fromtimestamp(timestamp))
            values.append(cValue_inactive + offset)
            # print(datetime.fromtimestamp(timestamp - 1), cValue_active)
            # print(datetime.fromtimestamp(timestamp), cValue_inactive)
        else :
            last_activity.append(datetime.fromtimestamp(timestamp - 1))
            values.append(cValue_inactive + offset)
            last_activity.append(datetime.fromtimestamp(timestamp))
            values.append(cValue_active + offset)
            # print(datetime.fromtimestamp(timestamp - 1), cValue_inactive)
            # print(datetime.fromtimestamp(timestamp), cValue_active)

        if state == cValue_active:
            display=True
    # first xy
    last_activity.append(datetime.fromtimestamp(to_time))
    values.append(values[-1])

    #last_activity
    if display :
        plt.plot(last_activity, values, '-', label=host)
        plt.legend()
    return display

def get_jpg_file(path,from_time,to_time):
    plt.cla()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
    db=Database(path)
    hosts=db.get_hosts()
    db.close()
    offset = 1
    #print(hosts)
    for host in hosts:
        if generate_graph(path,plt, host[0], offset,from_time,to_time):
            offset += 1.5
    plt.gcf().autofmt_xdate()
    plt.savefig('static/images/lastday.png')
    archive_filename='static/archive/'+str(from_time)+'_'+str(to_time)+".png"
    plt.savefig(archive_filename)

if __name__ == '__main__':
    database = '/home/freebox/hosts.db'
    # last 24 hours
    to_time=int(datetime.timestamp(datetime.now()))
    from_time=1738075801
    get_jpg_file('new.db',from_time,to_time)

