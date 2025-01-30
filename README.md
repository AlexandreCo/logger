# logger

## install pip

```
sudo apt update
sudo apt-get install python3-pip
```

## install freebox-api

```
python3 -m venv venv/
venv/bin/pip install freebox-api
```

## clone freebox-logger

```
mkdir freebox-api
cd freebox-api
git clone git@github.com:AlexandreCo/logger.git tests/
```

## crontab freebox-logger every 5min

```
crontab -e
*/5 * * * * /home/freebox/venv/bin/python /home/freebox/freebox-api/tests/freebox_log_host.py
```

## install flask

```
~/venv/bin/pip install flask
```

## install matplotlib

```
~/venv/bin/pip install matplotlib
```

## Run flask server

```
$ cat server.sh
#!/bin/bash
cd /home/freebox/freebox-api/tests/flask
/home/freebox/venv/bin/flask --app '/home/freebox/freebox-api/tests/flask/log_server.py'  run --host=0.0.0.0
```

## autostart server

```
crontab -e
@reboot /home/freebox/server.sh
```

## take snapshot everyday

```
crontab -e
0 0 * * * curl 127.0.0.1:5000
```
