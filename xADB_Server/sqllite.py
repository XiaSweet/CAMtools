import sqlite3
import adblib as adb
import time
#格式美化
from prettytable import PrettyTable
from sqllib import main as sqls
print("正在初始化设备数据库。。。。")
sqls.setup()
say=PrettyTable(['设备序号','映射端口','设备标识','设备id'])
temp=1
port=600
conn = sqlite3.connect('device_name.db')
cursor = conn.cursor()
devices=adb.devices()
for i in devices: #初始化设备内容
    try:
        sql=f"SELECT port FROM devices WHERE device_id='{i}'"
        sql=cursor.execute(sql)
        values = sql.fetchall()
        port=values[0][0]
    except IndexError:
        while True: #寻找空白端口
            try:
                sql=f"SELECT port FROM devices WHERE port='{port}'"
                sql=cursor.execute(sql)
                sql=sql.fetchall()
                if sql.sort() == None:
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
            except sqlite3.IntegrityError:
                port=port+1
                time.sleep(0.5)
    conn.commit()
devices=sqls.count()
sql=f"SELECT * FROM devices"
sql=cursor.execute(sql)
values = sql.fetchall()
temp=1
for i in values:  #i[0]=port,i[1]=device_id,i[2]=name
    try:
        #sql=f"SELECT kinkname FROM devices WHERE device_id='{i}'"
        if i[2]==None:
            say.add_row([[temp],i[0],i[1],'无'])
        else:
            say.add_row([[temp],i[0],i[1],i[2]])
    except IndexError:
        say.add_row([[temp],i[0],i[1],'无'])
    finally:
        temp=temp+1
print("当前登记的设备信息：")
print(say)
while True:
    try: # 先开始单独写入 '''insert语句 把一个新的行插入到表中 into'''
        device_id = input("输入你需要标记的设备序号：")
        device_id=values[int(device_id)-1][1]
        kinkname = input('输入设备的备注:') 
        sql = f' update devices set kinkname = "{kinkname}" where device_id= "{device_id}" '
        cursor.execute(sql)
        print(f"设备标识：{kinkname} 成功标记到 {device_id}，3秒后即将结束程序")
        conn.commit()
        time.sleep(3)
        break
    except (ValueError,IndexError):
        print("您输入的设备序号有误，请核对后重新输入QaQ")
        time.sleep(3)
        continue
    except Exception as e:
        print(f"出现错误了，请留意错误提示：{repr(e)}")
        time.sleep(3)
        cursor.close()
        exit()
cursor.close()