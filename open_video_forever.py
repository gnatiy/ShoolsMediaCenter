import os
import datetime
import time
import mouse
import win32api
import win32gui
import pyperclip
import keyboard
from screeninfo import get_monitors


def setEngLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return (result)

def shutdown_cmd(command: str):
    delay = 0.5
    setEngLayout()
    keyboard.press('win')
    time.sleep(delay)
    keyboard.press_and_release('r')
    time.sleep(delay)
    keyboard.release('win')
    keyboard.press_and_release('backspace')
    time.sleep(delay)

    keyboard.press_and_release('c')
    keyboard.press_and_release('m')
    keyboard.press_and_release('d')
    time.sleep(delay)
    keyboard.press_and_release('enter')
    time.sleep(3)

    keyboard.press_and_release('enter')
    time.sleep(3)

    pyperclip.copy(command)
    time.sleep(delay)
    keyboard.press('ctrl')
    time.sleep(delay)
    keyboard.press_and_release('v')
    time.sleep(delay)
    keyboard.release('ctrl')
    time.sleep(delay)
    keyboard.press_and_release('enter')

    keyboard.press('alt')
    time.sleep(delay)
    keyboard.press_and_release('F4')
    time.sleep(delay)
    keyboard.release('alt')

screen_width = 0
screen_height = 0
monitors = get_monitors()
for monitor in monitors:
    if monitor.is_primary:
        screen_width = int(monitor.width)
        screen_height = int(monitor.height)
print(screen_width, screen_height)
delay = 0.5
file = open('startup_videos.txt', 'r', encoding='utf-8')
hymn = file.readline()
hymn_delay = int(file.readline().split(' ')[1])
quantity_of_videos = int(file.readline().split(' ')[1])
videos = list()
videos_delay = list()
is_video = False
was_no_hymn = True
play_videos = False
reload_file = False
was_black_screen = False

for i in range(quantity_of_videos):
    videos.append(file.readline())
    videos_delay.append(int(file.readline()))
command = str(file.readline())[:-1]
flag_video = int(file.readline().split(' ')[1])
flag_hymn = int(file.readline().split(' ')[1])
double_click_var = int(file.readline().split(' ')[1])
file.readline()
monday = int(file.readline().split(' ')[0])
tuesday = int(file.readline().split(' ')[0])
wednesday = int(file.readline().split(' ')[0])
thursday = int(file.readline().split(' ')[0])
friday = int(file.readline().split(' ')[0])
saturday = int(file.readline().split(' ')[0])
sunday = int(file.readline().split(' ')[0])
file.close()

while True:
    timenow = str(datetime.datetime.now()).split(' ')[1]
    print(timenow[:2], timenow[3:5])

    if keyboard.is_pressed('1') and keyboard.is_pressed('2'):
        print('Early video initiated')
        is_video = True
        was_no_hymn = False

    if was_no_hymn and timenow[:2] == '08' and timenow[3:5] == '00':
        if flag_hymn == 1:
            if int(datetime.datetime.weekday(datetime.datetime.now())) == 0:
                if was_black_screen:
                    keyboard.press_and_release('F11')
                    time.sleep(delay)
                    keyboard.press('alt')
                    time.sleep(delay)
                    keyboard.press_and_release('F4')
                    time.sleep(delay)
                    keyboard.release('alt')
                    was_black_screen = False
                print("Starting hymn")
                os.startfile(hymn[:-1])
                mouse.move(screen_width // 2, screen_height // 2)
                if double_click_var == 1:
                    time.sleep(5)
                    mouse.double_click()
                time.sleep(hymn_delay * 60)
                is_video = True
                was_no_hymn = False
            else:
                print(f'Variable flag hymn is {flag_hymn} and today is not Monday')
                is_video = True
                was_no_hymn = False
        else:
            print(f'Variable flag hymn is {flag_hymn}')
            is_video = True
            was_no_hymn = False

    if is_video:
        if flag_video == 1:
            if was_black_screen:
                keyboard.press_and_release('F11')
                time.sleep(delay)
                keyboard.press('alt')
                time.sleep(delay)
                keyboard.press_and_release('F4')
                time.sleep(delay)
                keyboard.release('alt')
                was_black_screen = False
            day_of_the_week = int(datetime.datetime.weekday(datetime.datetime.now()))
            if day_of_the_week == 0:
                if monday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Monday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 1:
                if tuesday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Tuesday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 2:
                if wednesday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Wednesday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 3:
                if thursday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Thursday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 4:
                if friday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Friday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 5:
                if saturday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Saturday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
            elif day_of_the_week == 6:
                if sunday == 1:
                    play_videos = True
                    is_video = False
                else:
                    print('No playing on this Sunday')
                    is_video = False
                    reload_file = True
                    time.sleep(61)
        else:
            print(f'Flag_video is {flag_video}')
            time.sleep(61)
            is_video = False
            reload_file = True

    while play_videos:
        for i in range(len(videos)):
            print("Starting video")
            os.startfile(videos[i][:-1])
            mouse.move(screen_width // 2, screen_height // 2)
            if double_click_var == 1:
                time.sleep(5)
                mouse.double_click()
            time.sleep(videos_delay[i] * 60)
            timenow = str(datetime.datetime.now()).split(' ')[1]
            print(timenow[:2], timenow[3:5])
            if int(timenow[:2]) >= 17 and int(timenow[3:5]) >= 00:
                print('Day ended')
                play_videos = False
                reload_file = True
                break

    if reload_file:
        file = open('startup_videos.txt', 'r', encoding='utf-8')
        hymn = file.readline()
        hymn_delay = int(file.readline().split(' ')[1])
        quantity_of_videos = int(file.readline().split(' ')[1])
        videos = list()
        videos_delay = list()
        is_video = False
        was_no_hymn = True
        play_videos = False
        reload_file = False
        was_black_screen = True

        for i in range(quantity_of_videos):
            videos.append(file.readline())
            videos_delay.append(int(file.readline()))
        command = str(file.readline())[:-1]
        flag_video = int(file.readline().split(' ')[1])
        flag_hymn = int(file.readline().split(' ')[1])
        double_click_var = int(file.readline().split(' ')[1])
        file.readline()
        monday = int(file.readline().split(' ')[0])
        tuesday = int(file.readline().split(' ')[0])
        wednesday = int(file.readline().split(' ')[0])
        thursday = int(file.readline().split(' ')[0])
        friday = int(file.readline().split(' ')[0])
        saturday = int(file.readline().split(' ')[0])
        sunday = int(file.readline().split(' ')[0])
        file.close()
        os.startfile('black_screen.jpg')
        time.sleep(15)
        keyboard.press_and_release('F11')
        time.sleep(5)
        mouse.move(screen_width + 100, screen_height // 2)

    time.sleep(1)
