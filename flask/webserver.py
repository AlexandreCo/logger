from flask import Flask, render_template, request
from export import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    totime = request.args.get('to')
    if totime == None:
        to_time = int(datetime.timestamp(datetime.now()))
    else:
        to_time = int(totime)

    fromtime = request.args.get('from')
    if fromtime == None:
        # last 24 hours
        from_time = to_time - 24 * 60 * 60
    else:
        from_time = int(fromtime)

    get_jpg_file('/home/freebox/hosts.db',from_time, to_time)
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data():
    host = request.args.get('host')
    if host == None:
        return "please give host"

    totime = request.args.get('to')
    if totime == None:
        to_time = int(datetime.timestamp(datetime.now()))
    else:
        to_time = int(totime)

    fromtime = request.args.get('from')
    if fromtime == None:
        from_time = to_time - 24 * 60 * 60
    else:
        from_time = int(fromtime)

    print(host, from_time, to_time)

    html = "host : " + host + "<br>" + str(datetime.fromtimestamp(int(from_time))) + "<br>" + str(
        datetime.fromtimestamp(int(to_time))) + "<br>"

    # last 24 hours
    # to_time=int(datetime.timestamp(datetime.now()))
    # from_time=to_time-24*60*60
    db = Database()
    rows = db.get_host_data(host)
    db.close()
    html += "<table class=\"table\">"
    html += "<tr><th>Timestamp</th><th>Device id</th><th>Name</th><th>type</th><th>First activity</th><th>Last activity</th><th>Last time reachable</th>"
    for row in rows:
        html += "<tr><td>" + str(datetime.fromtimestamp(int(row[1]))) + "</td><td>" + row[2] + "</td><td>" + row[
            3] + "</td><td>" + row[4] + "</td><td>" + str(datetime.fromtimestamp(int(row[5]))) + "</td><td>" + str(
            datetime.fromtimestamp(int(row[6]))) + "</td><td>" + str(datetime.fromtimestamp(int(row[7]))) + "</td></tr>"
    html += "</table><style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>"
    return html
