import sqlite3
import server as adb
import time
from prettytable import PrettyTable #格式美化
class main: #基础运行时
    def setup(): #初始化数据库组件,用作基础运行库
        try:
            conn = sqlite3.connect('device_name.db')
            cursor = conn.cursor()
            devices=adb.check_devices()
            cursor = conn.execute("select port,device_id,kinkname from devices")
        except sqlite3.OperationalError:
            sql = '''CREATE TABLE IF NOT EXISTS devices (
                    port int unique,
                    device_id VARCHAR primary key,
                    kinkname VARCHAR)'''
            cursor.execute(sql)
        except Exception as e:
            cursor.close()
            print("出现其他错误了：",e)
            return 1,e
        finally:
            cursor.close()
        return 0,"ok"
    def count():  #计数类基础组件
        conn = sqlite3.connect('device_name.db')
        cursor = conn.cursor()
        sql=f"SELECT COUNT(*) FROM devices"
        sql=cursor.execute(sql)
        sql = sql.fetchall()
        return sql[0][0]
class search: #搜索类函数
    def lib(where,name="device_id"): #基础搜索类参数,name可选代表搜索类型，不填默认id
        try:
            conn = sqlite3.connect('device_name.db')
            cursor = conn.cursor()
            sql=f"SELECT * FROM devices WHERE {name} = '{where}'"
            sql=cursor.execute(sql)
            sql = sql.fetchall()
            temp={}
            if sql==[]:  #查询无结果
                return 2,"None"
            else: #查询出结果
                temp["port"]=sql[0][0]
                temp["device_id"]=sql[0][1]
                temp["setname"]=sql[0][2]
                return 1,temp
        except Exception as e:
            return 0,e
    def id(did): #根据设备唯一id号搜索信息,返回id下属的信息
        return search.lib(did)
    def kinkname(did):
        return search.lib(did,name="kinkname")
class write: #写入类函数
    import sqlite3
    def kinkname(device_id,kinkname):  #写入数据库
        try: # 先开始单独写入 '''insert语句 把一个新的行插入到表中 into'''
            conn = sqlite3.connect('device_name.db')
            cursor = conn.cursor()
            sql = f'update devices set kinkname = "{kinkname}" where device_id= "{device_id}" '
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(f"出现错误了，错误提示：{repr(e)}")
            time.sleep(3)
        finally:
            cursor.close()