from flask import Flask, redirect, url_for,render_template,make_response
from flask_apscheduler import APScheduler
import adblib as adb
import time
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    print('创建的临时目录：', tmpdir)
    app = Flask(__name__)
    @app.route('/')
    def index(devices_info=[]):
       return render_template('index.html',device=device_db)
    @app.route('/gettime/',methods=['POST'])
    def gettime():
        return time.ctime()
    @app.route('/devices/',methods=['get','POST'])
    def connect_devices():
        return str(len(adb.devices()))
    #定义设备参数类id
    @app.route("/devices/<deviceID>/screen/")
    def get_screen(deviceID):
        import pathlib
        path = pathlib.Path(f"/{tmpdir}/{deviceID}.png")
        path = path.exists()
        if path == True:
            print("获取本地的缓存")
            import base64
            with open(f"{tmpdir}/{deviceID}.png","rb") as f:
                base64_data = base64.b64encode(f.read()).decode('ascii')
                return base64_data
        else:
            temp=adb.xtools.getscreen(tmpdir,deviceID)
            return str(temp)
        #return render_template('screen.html',scr=temp)
    @app.route("/devices/<deviceID>/localip/",methods=['get','POST'])
    def get_localip(deviceID):
        return adb.xtools.localip(deviceID)
    import services as ser
    def task():
        scheduler = APScheduler()
        scheduler.init_app(app)
        # 定时任务的格式
        scheduler.add_job(func=ser.get_devices_screen,args=[tmpdir],trigger='interval',seconds=30, id='get_screen')
        scheduler.start()
    print(f"小提示：当前在线adb设备链接数量为{len(adb.devices())}个")
    print("正在初始化Server设备数据库。。。。")
    from prettytable import PrettyTable
    import sqllib as sqls
    import sqlite3
    temp=adb.devices()
    sqls.main.setup()
    device_db=[]
    port=600
    task()
    for i in temp: #初始化设备内容
        sql=sqls.search.id(i)
        if sql[0]==1:
            device_db.append(sql[1])
        elif sql[0]==2:
            print("警告:没有在数据库中查询到结果")
            while True: #寻找空白端口
                conn = sqlite3.connect('device_name.db')
                cursor = conn.cursor()
                sql=f"SELECT COUNT(port) FROM devices WHERE port='{port}'"
                sql=cursor.execute(sql)
                sql=sql.fetchall()
                if sql[0][0] == 0:
                    sql = ''' insert into devices
                      (port, device_id)
                      values
                      (:端口, :设备id)'''
                    cursor.execute(sql,{'端口':port, '设备id':i})
                    sql = ''' update devices set port = ":端口" where device_id= ":设备id" '''
                    cursor.execute(sql,{'端口':port, '设备id':i})
                    cursor.fetchall()
                    print(f"为未注册设备id：{i} 分配 {port} 端口")
                    break
                else:
                    port=port+1
                    time.sleep(0.5)
            conn.commit()
            cursor.close()
        else:
            print(f"函数出现错误了：{sql[1]}")
    print("设备数据库初始化成功owo")
    #开启Server
    if __name__ == '__main__':
        ser.get_ace_kickname()
        app.run(host='0.0.0.0',debug = False)