import os
import subprocess

class xtools: #Xiasweet ADB tools
    def localip(devices): #获取本机设备ipv4地址,返回设备ip
        try:
            log=shell(devices,"ip addr show wlan0")
            import re
            ip=re.findall(r'inet\s(\d+?\.\d+?\.\d+?\.\d+?)/\d+',log)
            return ip[0]
        except IndexError:
            return "False"

def overtcp(port,deviceid): #映射TCP运行时
    subprocess.call(f"nohup adbkit usb-device-to-tcp -p {port} {deviceid} >/dev/null 2>log &", shell=True)
def devices():
    '''
    检查adb 设备，并返回设备sn list
    :return: 设备sn list
    '''
    adb_list=[]
    ret =os.popen('adb devices').readlines()
    if len(ret) ==1:
        print('Warning：未识别到adb 设备...')
        return adb_list
    else:
        for n in ret:
            if '\tdevice\n' in n:
                adb=str(n).strip().split('\tdevice')[0].strip()
                adb_list.append(str(adb))
        #print('adb设备数量={}，adb_list={}'.format(len(adb_list), adb_list))
        return adb_list
def shell(devices,shell):
    '''
    操作指定设备执行指令,需要设备id与执行指令
    :return: 设备 执行的指令
    '''
    ret =subprocess.getoutput(f'adb -s {devices} shell {shell}')
    return ret