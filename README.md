# logger
## install pip
```
sudo apt update
sudo apt-get install python3-pip
```
## install freebox-api
```
python3 -m venv venv/
venv/bin/pip install freebox-api
```
## clone freebox-logger
```
mkdir freebox-api
cd freebox-api
git clone git@github.com:AlexandreCo/logger.git tests/
```
## crontab freebox-logger every 5min
```
crontab -e
```
write
```
*/5 * * * * /home/freebox/venv/bin/python /home/freebox/freebox-api/tests/freebox_log_host.py
```

