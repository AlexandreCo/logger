import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from database import *

def get_data(path,host,offset,from_time,to_time):
    db = Database(path)
    rows = db.get_host_data(host)
    db.close()
    last_activity = []
    values = []
    display=False
    remove_last=True
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
            if state == cValue_active:
                values[0]=(cValue_inactive + offset)
            else :
                values[0]=(cValue_active + offset)
        else :
            if timestamp < to_time:
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
            else :
                remove_last = False


        if state == cValue_active:
            display=True
    # first xy
    last_activity.append(datetime.fromtimestamp(to_time))
    values.append(values[-1])

    #last_activity
    if display and remove_last :
        last_activity.pop()
        last_activity.pop()
        values.pop()
        values.pop()

    return display, values, last_activity


def generate_graph(path,plt,host,offset,from_time,to_time):
    #display only if host is active during selected time range
    display, states, times = get_data(path,host,offset,from_time,to_time)
    #last_activity
    if display :
        plt.plot(times, states, '-', label=host)
    return display

def get_jpg_file(path,from_time,to_time):
    plt.cla()
    plt.subplots()
    plt.subplots_adjust(left=0.200)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
    db=Database(path)
    hosts=db.get_hosts()
    db.close()
    offset = 1
    y_order_label=[]
    y_order_pos=[]
    list_hosts=[]
    for host in hosts:
        if generate_graph(path,plt, host[0], offset,from_time,to_time):
            y_order_label.append(host[0])
            y_order_pos.append(offset)
            offset += 1.5
            list_hosts.append(host[0])

    plt.gcf().autofmt_xdate()
    plt.gca().yaxis.set_major_locator(ticker.FixedLocator(y_order_pos))
    plt.gca().yaxis.set_major_formatter(ticker.FixedFormatter(y_order_label))
    plt.ylim(bottom=0)

    plt.savefig('static/images/lastday.png')
    archive_filename='static/archive/'+str(from_time)+'_'+str(to_time)+".png"
    plt.savefig(archive_filename)
    #plt.show()
    return list_hosts

if __name__ == '__main__':
    # last 24 hours
    to_time=int(datetime.timestamp(datetime.now()))
    from_time=to_time-60*60
    get_jpg_file('hosts.db',from_time,to_time)

