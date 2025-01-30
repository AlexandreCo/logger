import sqlite3
from flask import Flask, render_template, request
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
    rows = get_data(host,from_time,to_time)
    html+="<table class=\"table\">"
    html+="<tr><th>Timestamp</th><th>Device id</th><th>Name</th><th>type</th><th>First activity</th><th>Last activity</th><th>Last time reachable</th>"
    for row in rows:
        html += "<tr><td>"+str(datetime.fromtimestamp(int(row[1])))+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td><td>"+row[4]+"</td><td>"+str(datetime.fromtimestamp(int(row[5])))+"</td><td>"+str(datetime.fromtimestamp(int(row[6])))+"</td><td>"+str(datetime.fromtimestamp(int(row[7])))+"</td></tr>"
    html+="</table><style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>"
    return html

database='/home/freebox/hosts.db'
def generate_graph(plt,host,value,from_time,to_time):
    rows = get_data(host,from_time,to_time)
    last_activity = []
    for row in rows:
        last_activity.append(datetime.fromtimestamp(int(row[6])))

    #last_activity
    values = [value for ts in last_activity]
    plt.plot(last_activity, values, 'o', label=host)
    plt.legend()

def get_data(host,from_time,to_time):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql='SELECT * FROM devices where primary_name is "' + host + '" and timestamp between ' + str(from_time) + ' and ' + str(to_time)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def getHosts(from_time,to_time):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql="SELECT DISTINCT primary_name FROM devices where timestamp between " + str(from_time) + " and " + str(to_time)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_jpg_file(from_time,to_time):
    plt.cla()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
    hosts=getHosts(from_time,to_time)
    value = 1
    for host in hosts:
        generate_graph(plt, host[0], value,from_time,to_time)
        value += 1
    plt.gcf().autofmt_xdate()
    plt.savefig('static/images/lastday.png')
    archive_filename='static/archive/'+str(from_time)+'_'+str(to_time)+".png"
    plt.savefig(archive_filename)

if __name__ == '__main__':
    # last 24 hours
    to_time=int(datetime.timestamp(datetime.now()))
    from_time=to_time-24*60*60
    get_jpg_file(from_time,to_time)

