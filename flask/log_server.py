import sqlite3
from flask import Flask, render_template, request
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from database import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():

    totime = request.args.get('to')
    if totime == None:
        to_time = int(datetime.timestamp(datetime.now()))
    else :
        to_time = int(totime)

    fromtime = request.args.get('from')
    if fromtime == None:
        # last 24 hours
        from_time=to_time-24*60*60
    else:
        from_time = int(fromtime)

    get_jpg_file(from_time,to_time)
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    host = request.args.get('host')
    if host == None:
        return "please give host"

    totime = request.args.get('to')
    if totime == None:
        to_time = int(datetime.timestamp(datetime.now()))
    else :
        to_time = int(totime)

    fromtime = request.args.get('from')
    if fromtime == None:
        from_time=to_time-24*60*60
    else:
        from_time = int(fromtime)

    print(host,from_time,to_time)
    
    html = "host : " + host + "<br>" + str(datetime.fromtimestamp(int(from_time))) + "<br>"  + str (datetime.fromtimestamp(int(to_time))) + "<br>"

    # last 24 hours
    # to_time=int(datetime.timestamp(datetime.now()))
    # from_time=to_time-24*60*60
    db = Database()
    rows = db.get_host_data(host,from_time,to_time)
    db.close()
    html+="<table class=\"table\">"
    html+="<tr><th>Timestamp</th><th>Device id</th><th>Name</th><th>type</th><th>First activity</th><th>Last activity</th><th>Last time reachable</th>"
    for row in rows:
        html += "<tr><td>"+str(datetime.fromtimestamp(int(row[1])))+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td><td>"+row[4]+"</td><td>"+str(datetime.fromtimestamp(int(row[5])))+"</td><td>"+str(datetime.fromtimestamp(int(row[6])))+"</td><td>"+str(datetime.fromtimestamp(int(row[7])))+"</td></tr>"
    html+="</table><style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>"
    return html

database='/home/freebox/hosts.db'
def generate_graph(plt,host,offset,from_time,to_time):
    #display only if host is active during selected time range
    display = False
    db = Database()
    rows = db.get_host_data(host)
    db.close()
    last_activity = []
    values = []
    # first xy
    last_activity.append(datetime.fromtimestamp(from_time))
    values.append(rows[0][cDevices_values]+offset)

    for row in rows:
        state=row[cDevices_values]


        if values[-1] == state + offset :
            #last elements is the same as new one
            last_activity.append(datetime.fromtimestamp(int(row[cDevices_timestamp])))
            values.append(state + offset)
        else :
            if state == cValue_active :
                last_activity.append(datetime.fromtimestamp(int(row[cDevices_timestamp] - 1)))
                values.append(cValue_inactive + offset)
                last_activity.append(datetime.fromtimestamp(int(row[cDevices_timestamp])))
                values.append(cValue_active + offset)
            else :
                last_activity.append(datetime.fromtimestamp(int(row[cDevices_timestamp] - 1)))
                values.append(cValue_active + offset)
                last_activity.append(datetime.fromtimestamp(int(row[cDevices_timestamp])))
                values.append(cValue_inactive + offset)

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

def get_jpg_file(from_time,to_time):
    plt.cla()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
    db=Database()
    hosts=db.get_hosts()
    db.close()
    offset = 1
    for host in hosts:
        if generate_graph(plt, host[0], offset,from_time,to_time):
            offset += 1.5
    plt.gcf().autofmt_xdate()
    plt.savefig('static/images/lastday.png')
    archive_filename='static/archive/'+str(from_time)+'_'+str(to_time)+".png"
    plt.savefig(archive_filename)

if __name__ == '__main__':
    # last 24 hours
    to_time=int(datetime.timestamp(datetime.now()))
    from_time=to_time-24*60*60
    get_jpg_file(from_time,to_time)

