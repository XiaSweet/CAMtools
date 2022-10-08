import subprocess
import time

print("使用须知：\n请提前确定好你需要链接的设备数！")
while True:
    '''
    下面2行代码是交互界面才需要填的
    iphost=input("请输入需要链接的IP源：")
    ip范围=input("请输入需要尝试链接的设备数(0-100)：")
    下面的代码按需填写 iphost是ip链接源，ip范围是尝试链接的设备数
    '''
    iphost="192.168.198.131"
    iphost1="10.14.240.66"
    ip范围=6
    try:
        ip范围=int(ip范围) #转换数字
    except:
        print("出现范围错误了，请重新选择")
    else:
        break #调验证
print("即将链接，请稍等,请确保系统变量含有adb调试程序。。。。")
subprocess.call(f"adb disconnect ", shell=True)
time.sleep(1)
temp=0
while temp<ip范围:
    subprocess.call(f"adb connect {iphost}:{600+temp} ", shell=True)
    time.sleep(0.5)
    temp=temp+1
temp=0
while temp<ip范围:
    subprocess.call(f"adb connect {iphost}:{600+temp} ", shell=True)
    time.sleep(0.5)
    temp=temp+1
print("设备链接完毕，请使用ACE群控或Qtscrcpy继续群控操作\n记得不用的时候使用” adb disconnect “端开网络链接")
time.sleep(3)