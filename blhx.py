import  subprocess
import os
import cv2
import time
import random


def cmd(command):
    return (subprocess.check_output(command,shell=True).decode('gbk').strip())
def get_pos(target_img_path,find_img_path,accuracy=0.7):
    target_img = cv2.imread(target_img_path)
    find_img = cv2.imread(find_img_path)
    find_height, find_width, find_channel = find_img.shape[::]

    # 模板匹配
    result = cv2.matchTemplate(target_img, find_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 计算位置
    pointUpLeft = max_loc
    pointLowRight = (max_loc[0] + find_width, max_loc[1] + find_height)
    pointCentre = (max_loc[0] + (find_width / random.randint(2,10)), max_loc[1] + (find_height / random.randint(2,10)))
    if max_val>accuracy:
        return pointCentre
    else:
        raise Exception("can not find target")

class ADB:
    def __init__(self):
        self.devices=[]
        self.device=None
        self.get_devices()
    def get_devices(self):
        cmd_output=cmd('adb devices')
        for line in cmd_output.split('\n')[1:]:
            if 'device' in line:
                self.devices.append((line.split()[0]))
        for device in self.devices:
            # ?print('已连接设备%s'%device)
            pass
    def connect_device(self,device='d52112ab'):
        if  device in self.devices:
            self.device=device
            print('连接%s设备成功'%device)
        else:
            print("设备无法连接")
    def list_info(self):
        print('型号',cmd('adb shell getprop ro.product.model'))
        print('分辨率',cmd('adb shell wm size'))
    def screencap(self,store_path=os.getcwd(),filename='sc.png'):
        file_path=os.path.join(store_path,filename)
        # print('adb exec-out screencap -p > % s'%file_path)
        cmd('adb exec-out screencap -p > % s'%file_path)
        # time.sleep(3)
        # print('截图保存在%s'%file_path)
        return file_path
    def click(self,point):
        # print('click',point)
        cmd('adb shell input tap %s %s'%(point[0],point[1]))
        time.sleep(1)
    def click_r_point(self,point):
        cmd('adb shell input tap %s %s' % (point[0]+random.randint(0,10), point[1]+random.randint(0,10)))
        time.sleep(1)
    def click_r_point(self,x,y):
        cmd('adb shell input tap %s %s' % (x+random.randint(0,10), y+random.randint(0,10)))
        time.sleep(1)
    def swipe(self,point1,point2):
        cmd('adb shell input swipe %s %s %s %s' %
            (point1[0] + random.randint(0, 10), point1[1] + random.randint(0, 10))
            ,point2[0]+random.randint(0, 10),point2[1]+random.randint(0, 10))
        time.sleep(1)
    def swipe(self, x1, y1,x2,y2):
        cmd('adb shell input swipe %s %s %s %s' %
            (x1 + random.randint(0, 10), y1+ random.randint(0, 10)
            , x2+ random.randint(0, 10), y2+random.randint(0, 10)))
        time.sleep(1)
    def click_target(self,target):
        target_path=os.path.join('./target',"%s.png"%target)
        sc_path = self.screencap()
        point = get_pos(sc_path,target_path)
        self.click(point)
        print(target,point)
    def check_target(self, target,accuracy=0.7):
        target_path = os.path.join('./target', "%s.png" % target)
        sc_path = self.screencap()
        try:
            point = get_pos(sc_path, target_path,accuracy)
            print(target,point)
            return point
        except:
            return False

    def move(self,target,target_point):
        point=self.check_target(target,accuracy=0.5)
        self.swipe(point[0], point[1], target_point[0], point[1])
        self.swipe(target_point[0], point[1],target_point[0], target_point[1])

adb=ADB()
adb.connect_device(device='d52112ab')
adb.list_info()

def attack(enemy,exit_enemy):
    adb.click(exit_enemy)
    time.sleep(5)
    while(not adb.check_target('attack')):
        if adb.check_target('avoid'):
            adb.click_target('avoid')
        adb.click(exit_enemy)
    adb.click_r_point(1645, 964)
    time.sleep(25)
    while (not adb.check_target('end_battle')):
        time.sleep(5)
    while (not adb.check_target('end_battle_firm')):
        time.sleep(1)
        adb.click_r_point(940, 783)
    adb.click_r_point(1566, 1020)
team1_count=0
def attack_ship(shipname):
    global team1_count
    exit_enemy = adb.check_target(shipname, 0.5)
    if exit_enemy:
        attack(shipname, exit_enemy)
        team1_count+= 1#如果要在函数中给全局变量赋值，需要用global关键字声明
    time.sleep(10)
    print('team1_count',team1_count)
    if team1_count == 5 :
        print('切换舰队')
        adb.click_target('switch_team')#切换舰队
while (True):
    time.sleep(10)
    print('选择6-4')
    adb.click_r_point(410,710)#选择6-4
    print('点击出击')
    adb.click_r_point(1382,764)#点击出击
    print('立即前往')
    adb.click_r_point(1568,908)#立即前往
    team1_count=0
    while(True):
        #解决地图问题
        for ship in ['enemy1', 'enemy2']:
            time.sleep(5)
            # if adb.check_target('map_error', 0.8):
            print('移动地图')
            #     adb.swipe(1642, 635, 896, 635)
            #     adb.swipe(1124, 635, 1124, 690)
            adb.move('island',(450,454))
            print('寻找boss')
            boss=adb.check_target('boss',0.7)
            if boss:
                print("找到boss")
                attack('boss',boss)
                break
            print('攻击小船')
            attack_ship(ship)
# adb.click_r_point(7,255)#弹出左侧
#
# adb.click_r_point(253,135)#收石油
# adb.click_r_point(685,165)#收金币

# adb.click_r_point(1436,542)#返回主界面
#
# adb.click_r_point(1564,616)#出击