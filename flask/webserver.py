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

    display,datas,atimes=get_data('/home/freebox/hosts.db', host, 0, from_time, to_time)
    if not display :
        return "<h2>unknow host<h2>"

    html = "host : " + host + "<br>" + str(datetime.fromtimestamp(int(from_time))) + "<br>" + str(
        datetime.fromtimestamp(int(to_time))) + "<br>"


    html += "<table class=\"table\">"
    html += "<tr><th>Timestamp</th><th>state</th>"
    index=0
    for data in datas:
        print(atimes[index])
        if datas[index] == cValue_inactive :
            state='inactif'
        else:
            state = 'actif'

        html += "<tr><td>" + str(atimes[index]) + "</td><td>" + state + "</td></tr>"
        index += 1
    html += "</table><style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>"

    return html
