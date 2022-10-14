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
    def getscreen(deviceID):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            print('创建的临时目录：', tmpdir)
            execout(deviceID,f'screencap -p > screen.png ',cddir=tmpdir)
            #print(subprocess.call(f"cd {tmpdir}&& c: && dir", shell=True))
            import base64
            with open(f"{tmpdir}\screen.png","rb") as f:
                # b64encode是编码，b64decode是解码
                base64_data = base64.b64encode(f.read()).decode('ascii')
                # base64.b64decode(base64data)
                return base64_data

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
def shell(devices,shell,cddir='0'):
    '''
    操作指定设备执行指令,需要设备id与执行指令
    :return: 设备 执行的指令
    '''
    if cddir=='0':
        ret =subprocess.getoutput(f'adb -s {devices} shell {shell}')
    else:
        ret =subprocess.getoutput(f'cd {cddir} && c: && adb -s {devices} shell {shell}')
    return ret
def execout(devices,shell,cddir='0'):
    '''
    操作指定设备执行指令,需要设备id与执行指令
    :return: 设备 执行的指令
    '''
    if cddir=='0':
        ret =subprocess.getoutput(f'adb -s {devices} exec-out {shell}')
    else:
        ret =subprocess.getoutput(f'cd {cddir} && c: && adb -s {devices} exec-out {shell}')
    return ret

