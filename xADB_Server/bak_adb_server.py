import os
import subprocess

"""
下面是多线程需要执行的映射程序:adb_overtcp
使用@DeviceFarmer/adbkit 的adb映射组件
使用后台映射不会影响STF端的远程控制
注意这里只输出错误日志到log里
"""
def adb_overtcp(port,deviceid): 
    subprocess.call(f"nohup adbkit usb-device-to-tcp -p {port} {deviceid} >/dev/null 2>log &", shell=True)
def check_devices():
    '''
    检查adb 设备，并返回设备sn list
    
    :return: 设备sn list
    '''
    adb_list=[]
    ret =os.popen('adb devices').readlines()
    """print('ret={}'.format(ret))"""
    if len(ret) ==1:
        print('未识别到adb 设备...')
        return adb_list
    else:
        for n in ret:
            if '\tdevice\n' in n:
                adb=str(n).strip().split('\tdevice')[0].strip()
                adb_list.append(str(adb))
        #print('adb设备数量={}，adb_list={}'.format(len(adb_list), adb_list))
        return adb_list
 
 
if __name__ == '__main__':
    devices=check_devices()
    print(f"温馨提示：\n正在初始化，当前adb设备数量为{len(devices)}个，映射端口分别为600-{600+len(devices)}")
    import time
    port=600
    time.sleep(5)
    print("映射的端口      映射的设备id")
    for i in devices:
        print(f"{port}      {i}")
        adb_overtcp(port,i)
        port=port+1
    print("端口映射执行完毕，请在Windows客户端内使用一键链接！")