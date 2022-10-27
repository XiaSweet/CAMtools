# -*- coding: utf-8 -*-
import adblib as adb
import subprocess
def get_devices_screen(tmpdir):
    temp=adb.devices()
    for t in temp:
        adb.execout(t,f'screencap -p > temp.png ',cddir=tmpdir)
        #subprocess.getoutput(f'mv /{tmpdir}/temp.png /{tmpdir}/{t}.png')
        subprocess.getoutput(f'pngquant  /{tmpdir}/temp.png --force --skip-if-larger --output /{tmpdir}/{t}.png')
    print("设定的屏幕刷新任务执行完毕")
def get_ace_kickname():
    import tempfile
    from sqllib import write
    with tempfile.TemporaryDirectory() as tmpdir:
        temp=adb.devices()
        for deviceID in temp:
            adb.pull(deviceID,"/sdcard/devicesname.txt",f"/{tmpdir}/{deviceID}.txt")
            with open(f"{tmpdir}/{deviceID}.txt", mode='r',encoding='gbk') as did:
                f=did.read()
                write.kinkname(deviceID,f[2: ])
                did.close()
        print("ACE设备备注同步成功OwO")