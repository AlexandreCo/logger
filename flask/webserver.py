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

    list_hosts=get_jpg_file('/home/freebox/hosts.db',from_time, to_time)
    return render_template('index.html',hosts=list_hosts)


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

    display,list_datas,list_times=get_data('/home/freebox/hosts.db', host, 0, from_time, to_time)
    if not display :
        return "<h2>unknow host<h2>"

    datas=zip(list_datas,list_times)
    return render_template('data.html',datas=datas,host=host)
