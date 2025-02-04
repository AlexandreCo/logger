from flask import Flask, render_template, request
from export import *

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    form_data=request.form
    ts_to_time = int(datetime.timestamp(datetime.now()))
    ts_from_time = ts_to_time - 24 * 60 * 60
    if form_data :
        form_from_time=form_data.get('from')
        form_to_time = form_data.get('to')
        if form_to_time is not None:
            ts_to_time = datetime.timestamp(datetime.fromisoformat(form_to_time))
        if form_from_time is not None:
            ts_from_time = datetime.timestamp(datetime.fromisoformat(form_from_time))
    list_hosts=get_jpg_file('/home/freebox/hosts.db',ts_from_time, ts_to_time)
    iso_from=datetime.fromtimestamp(ts_from_time).isoformat()
    iso_to=datetime.fromtimestamp(ts_to_time).isoformat()
    return render_template('index.html',hosts=list_hosts,from_time=iso_from, to_time=iso_to)


@app.route('/data', methods=['GET','POST'])
def data():
    host = request.args.get('host')
    if host == None:
        return "please give host"
    form_data = request.form
    ts_to_time = int(datetime.timestamp(datetime.now()))
    ts_from_time = ts_to_time - 24 * 60 * 60
    if form_data:
        form_from_time = form_data.get('from')
        form_to_time = form_data.get('to')
        if form_to_time is not None:
            ts_to_time = datetime.timestamp(datetime.fromisoformat(form_to_time))
        if form_from_time is not None:
            ts_from_time = datetime.timestamp(datetime.fromisoformat(form_from_time))

    display,list_datas,list_times=get_data('/home/freebox/hosts.db', host, 0, ts_from_time, ts_to_time)
    if not display :
        return "<h2>unknow host<h2>"
    iso_from=datetime.fromtimestamp(ts_from_time).isoformat()
    iso_to=datetime.fromtimestamp(ts_to_time).isoformat()
    datas=zip(list_datas,list_times)
    return render_template('data.html',datas=datas,host=host,from_time=iso_from, to_time=iso_to)
