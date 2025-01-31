import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from database import *


def generate_graph(path,plt,host,offset,from_time,to_time):
    #display only if host is active during selected time range
    display = False
    db = Database(path)
    rows = db.get_host_data(host)
    db.close()
    last_activity = []
    values = []
    # first xy
    # last_activity.append(datetime.fromtimestamp(rows[0][cDevices_timestamp]))
    # values.append(rows[0][cDevices_values]+offset)
    for row in rows:
        state=row[cDevices_values]
        timestamp=int(row[cDevices_timestamp])

        if not len(values):
            if state == cValue_inactive:
                values.append(cValue_inactive + offset)
            else :
                values.append(cValue_active + offset)
            last_activity.append(datetime.fromtimestamp(from_time))

        if timestamp < from_time :
            if state == cValue_inactive:
                values[0]=(cValue_inactive + offset)
            else :
                values[0]=(cValue_active + offset)

        if state == cValue_inactive :
            last_activity.append(datetime.fromtimestamp(timestamp - 1))
            values.append(cValue_inactive + offset)
            last_activity.append(datetime.fromtimestamp(timestamp))
            values.append(cValue_active + offset)
        else :
            last_activity.append(datetime.fromtimestamp(timestamp - 1))
            values.append(cValue_active + offset)
            last_activity.append(datetime.fromtimestamp(timestamp))
            values.append(cValue_inactive + offset)

        if state == cValue_active:
            display=True
    # first xy
    last_activity.append(datetime.fromtimestamp(to_time))
    values.append(values[-1])

    #last_activity
    if display :
        # print(last_activity)
        # print(values)
        last_activity.pop()
        last_activity.pop()
        values.pop()
        values.pop()
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
    #plt.show()

if __name__ == '__main__':
    # last 24 hours
    to_time=int(datetime.timestamp(datetime.now()))
    from_time=to_time-60*60
    get_jpg_file('hosts.db',from_time,to_time)

