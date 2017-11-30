# Code to check if left or right mouse buttons were pressed
import win32api
import win32con
import time
from win32api import GetSystemMetrics

wide = GetSystemMetrics(0)
height = GetSystemMetrics(1)
mouseDown=2
mouseUp=1
move=0
#wide=1440
#height=2560

def record(ST=0.01):
    f=open('record.txt','w')
    f.close()
    f=open('record.txt','a')
    leftMouse=0x01
    rightMouse=0x02
  
    state_left = win32api.GetKeyState(leftMouse)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(rightMouse)  # Right button down = 0 or 1. Button up = -127 or -128
    record_button = win32api.GetKeyState(0x31)
    
    currentTime=time.time()
    #f.close()
    while True:
        a = win32api.GetKeyState(leftMouse)
        b = win32api.GetKeyState(rightMouse)
        c = win32api.GetKeyState(0x31)
        
        if c != record_button:
            time.sleep(0.5)
            f.close()
            return
        
        if time.time() - currentTime > ST:
            h_x, h_y = win32api.GetCursorPos()
            #f=open('record.txt','a')
            f.write("%.3f " % (time.time()-currentTime))
            f.write(' 0'  + ' ' + str(move) + ' ' + str(h_x) + ' ' + str(h_y) + '\n') 
            currentTime=time.time()
        
        if a != state_left:  # Button state changed
            state_left = a
            h_x, h_y = win32api.GetCursorPos()
            if a < 0:
                f.write("%.3f " % (time.time()-currentTime))
                f.write(' ' + str(leftMouse) + ' ' + str(mouseDown) + ' ' + str(h_x) + ' ' + str(h_y) + '\n') 
            else:
                f.write("%.3f " % (time.time()-currentTime))
                f.write(' ' + str(leftMouse) + ' ' + str(mouseUp) + ' ' + str(h_x) + ' ' + str(h_y) + '\n') 
            currentTime=time.time()    

        if b != state_right:  # Button state changed
            state_right = b
            h_x, h_y = win32api.GetCursorPos()
            if b < 0:
                f.write("%.3f " % (time.time()-currentTime))
                f.write(' ' + str(rightMouse) + ' ' + str(mouseDown) + ' ' + str(h_x) + ' ' + str(h_y) + '\n') 
            else:
                f.write("%.3f " % (time.time()-currentTime))
                f.write(' ' + str(rightMouse) + ' ' + str(mouseUp) + ' ' + str(h_x) + ' ' + str(h_y) + '\n') 
            currentTime=time.time() 
        time.sleep(0.001)
        
def play(loopTime = -1, sleepTime = 0.1):
    f = open('record.txt','r')
    lineStr = f.readlines()
    play_button = win32api.GetKeyState(0x32)
    while loopTime!=0 :
        loopTime = loopTime - 1
        for str in lineStr:
            currentEvent = str.split()
            c = win32api.GetKeyState(0x32)
            if c != play_button:
                time.sleep(0.5)
                f.close()
                return
                
            time.sleep(float(currentEvent[0]))
            if int(currentEvent[1])==0 :
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
                int(int(currentEvent[3])/wide*65535),int(int(currentEvent[4])/height*65535),0,0)
            if int(currentEvent[1])==1 :
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
                int(int(currentEvent[3])/wide*65535),int(int(currentEvent[4])/height*65535),0,0)
                if int(currentEvent[2])==mouseDown:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE,
                    int(int(currentEvent[3])/wide*65535),int(int(currentEvent[4])/height*65535),0,0)
                    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE,
                    #int(int(currentEvent[3])/wide*65535),int(int(currentEvent[4])/height*65535),0,0)
                if int(currentEvent[2])==mouseUp :
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE,
                    int(int(currentEvent[3])/wide*65535),int(int(currentEvent[4])/height*65535),0,0)
        time.sleep(sleepTime)

def _main():
    while True:
        toggled = False
        isPlay = False
        
        while win32api.GetKeyState(0x33) not in [0,1]:
            return
        
        while win32api.GetKeyState(0x31) not in [0,1]:
            toggled = True
            time.sleep(0.01)
        if toggled:
            toggled = False
            record()
            
        while win32api.GetKeyState(0x32) not in [0,1]:
            isPlay = True
            time.sleep(0.01)
        if isPlay:
            isPlay = False
            play()
        time.sleep(0.001)               

_main()
