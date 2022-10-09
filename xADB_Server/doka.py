from flask import Flask, redirect, url_for,render_template
from flask_apscheduler import APScheduler
import adb_server as adb
import time
app = Flask(__name__)
@app.route('/')
def index():
   return render_template('index.html')
   
@app.route('/gettime',methods=['POST'])
def gettime():
    return time.ctime()
    
@app.route('/devices',methods=['POST'])
def connect_devices():
    return str(len(adb.check_devices()))

def tishi():
    global devices
    devices=adb.check_devices()
    print(f"小提示：当前在线adb设备链接数量为{len(devices)}个")
    
def task():
    scheduler = APScheduler()
    scheduler.init_app(app)
    # 定时任务的格式
    scheduler.add_job(func=tishi, trigger='interval',seconds=30, id='devices')
    scheduler.start()


# 写在main里面，IIS不会运行
task()
tishi()
#开启Server
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)