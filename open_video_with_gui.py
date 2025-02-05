import os
import datetime
import time
import mouse
import keyboard
from screeninfo import get_monitors
from tkinter import *
from tkinter import ttk
import threading
from pymediainfo import MediaInfo
import re
from tkinter import filedialog

def get_video_duration(video_path):
    video = MediaInfo.parse(video_path)
    duration_secs = video.tracks[0].duration / 1000
    return round(duration_secs)

def replace_backslashes_regex(text):
  """Заменяет все символы \\ в строке на символы /, используя регулярные выражения."""
  return re.sub(r"\\", "/", text)

def open_multiple_files_dialog():
    """Открывает диалоговое окно выбора нескольких файлов и возвращает список путей к файлам."""
    root = Tk()
    root.withdraw()  # Скрыть главное окно tkinter
    file_paths = filedialog.askopenfilenames(title="Выберите файлы")
    root.destroy()
    return file_paths

bg = '#5C88E8'

class MY_WINDOW():
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1180x720")
        self.window.title("Автозапуск видео")
        self.window.resizable(False, False)
        self.window.config(bg=bg)

        self.video_files_tree = ttk.Treeview(self.window)
        self.terminal_tree = ttk.Treeview(self.window)

        self.load_data()
        self.create_video_file_tree()
        self.create_terminal_tree()
        self.create_buttons()

        thread_loop = threading.Thread(target=self.loop, daemon=True)
        thread_loop.start()

        self.window.mainloop()

    def create_video_file_tree(self):
        self.video_files_tree['columns'] = ('ID', 'video_file', 'duration')

        self.video_files_tree.column('#0', width=0, stretch=NO)
        self.video_files_tree.column('ID', anchor=CENTER, width=50)
        self.video_files_tree.column('video_file', anchor=W, width=515)
        self.video_files_tree.column('duration', anchor=W, width=90)

        self.video_files_tree.heading('#0', text='', anchor=W)
        self.video_files_tree.heading('ID', text='ID', anchor=CENTER)
        self.video_files_tree.heading('video_file', text='Video_file', anchor=CENTER)
        self.video_files_tree.heading('duration', text='Duration, m, s', anchor=CENTER)

        self.video_files_tree.configure(height=15)

        self.video_files_tree.place(x=10, y=10)

    def create_terminal_tree(self):
        self.terminal_tree['columns'] = ('current_log')

        self.terminal_tree.column('#0', width=0, stretch=NO)
        self.terminal_tree.column('current_log', anchor=W, width=250)

        self.terminal_tree.heading('#0', text='', anchor=W)
        self.terminal_tree.heading('current_log', text='Current log', anchor=CENTER)

        self.terminal_tree.configure(height=15)

        self.terminal_tree.place(x=680, y=10)

    def create_buttons(self):
        self.add_video_button = Button(self.window, text='Добавить файлы mp4', font='Arial 16', activebackground='blue', anchor=CENTER)
        self.add_video_button.place(x=10, y=350)

        self.delete_one_button = Button(self.window, text='Удалить выбранное видео', font='Arial 16', activebackground='blue', anchor=CENTER)
        self.delete_one_button.place(x=10, y=420)

        self.delete_all_button = Button(self.window, text='Удалить все видео', font='Arial 16', activebackground='blue', anchor=CENTER)
        self.delete_all_button.place(x=10, y =490)

        self.add_video_button.config(command=self.add_video_to_list)
        self.delete_one_button.config(command=self.remove_one_video)
        self.delete_all_button.config(command=self.delete_all_videos)

    def new_record_videos_tree(self, text, text2, text3):
        self.video_files_tree.insert(parent='', index='end', values=(str(text), str(text2), str(text3)))
        self.video_files_tree.yview_moveto(1.0)

    def new_record_terminal_tree(self, text):
        self.terminal_tree.insert(parent='', index='end', values=text)
        self.all_records = self.terminal_tree.get_children()
        if len(self.all_records) > 30:
            self.terminal_tree.delete(self.all_records[0])
        self.terminal_tree.yview_moveto(5.0)

    def load_data(self):
        self.screen_width = 0
        self.screen_height = 0
        self.monitors = get_monitors()
        for monitor in self.monitors:
            if monitor.is_primary:
                self.screen_width = int(monitor.width)
                self.screen_height = int(monitor.height)
        self.new_record_terminal_tree(str(self.screen_width) + 'x' + str(self.screen_height))
        self.delay = 0.5
        self.file = open('startup_videos.txt', 'r', encoding='utf-8')
        self.hymn = self.file.readline().strip()
        self.hymn_delay = int(self.file.readline().strip().split(' ')[1])
        self.quantity_of_videos = int(self.file.readline().split(' ')[1])
        self.videos = list()
        self.videos_delay = list()
        self.is_video = False
        self.was_no_hymn = True
        self.play_videos = False
        self.reload_file = False
        self.was_black_screen = False

        if self.video_files_tree.get_children():
            for record in self.video_files_tree.get_children(): self.video_files_tree.delete(record)
        for i in range(self.quantity_of_videos):
            self.videos.append(self.file.readline().strip())
            self.videos_delay.append(int(self.file.readline().strip()))
        for index, i in enumerate(self.videos):
            self.duration = get_video_duration(i)
            self.new_record_videos_tree(index + 1, i, f'{self.duration // 60}m {self.duration % 60}s')
        self.command = str(self.file.readline())[:-1]
        self.flag_video = int(self.file.readline().split(' ')[1])
        self.flag_hymn = int(self.file.readline().split(' ')[1])
        self.double_click_var = int(self.file.readline().split(' ')[1])
        self.file.readline()
        self.monday = int(self.file.readline().split(' ')[0])
        self.tuesday = int(self.file.readline().split(' ')[0])
        self.wednesday = int(self.file.readline().split(' ')[0])
        self.thursday = int(self.file.readline().split(' ')[0])
        self.friday = int(self.file.readline().split(' ')[0])
        self.saturday = int(self.file.readline().split(' ')[0])
        self.sunday = int(self.file.readline().split(' ')[0])
        self.file.close()

    def save_changes(self):
        pass

    def add_video_to_list(self):
        self.new_files = open_multiple_files_dialog()
        for file in self.new_files:
            self.duration = get_video_duration(file)
            self.new_record_videos_tree('***', file, f'{self.duration // 60}m {self.duration % 60}s')

    def remove_one_video(self):
        self.selected = self.video_files_tree.selection()[0]
        self.video_files_tree.delete(self.selected)

    def delete_all_videos(self):
        for record in self.video_files_tree.get_children(): self.video_files_tree.delete(record)

    def loop(self):
        while True:
            self.timenow = str(datetime.datetime.now()).split(' ')[1]
            self.new_record_terminal_tree(f'Time-->{str(self.timenow[:2])}:{str(self.timenow[3:5])}')

            if keyboard.is_pressed('1') and keyboard.is_pressed('2'):
                self.new_record_terminal_tree('Early_video_initiated')
                self.is_video = True
                self.was_no_hymn = False

            if self.was_no_hymn and self.timenow[:2] == '08' and self.timenow[3:5] == '00':
                if self.flag_hymn == 1:
                    if int(datetime.datetime.weekday(datetime.datetime.now())) == 0:
                        if self.was_black_screen:
                            keyboard.press_and_release('F11')
                            time.sleep(self.delay)
                            keyboard.press('alt')
                            time.sleep(self.delay)
                            keyboard.press_and_release('F4')
                            time.sleep(self.delay)
                            keyboard.release('alt')
                            self.was_black_screen = False
                        self.new_record_terminal_tree("Starting_hymn")
                        os.startfile(self.hymn[:-1])
                        mouse.move(self.screen_width // 2, self.screen_height // 2)
                        if self.double_click_var == 1:
                            time.sleep(5)
                            mouse.double_click()
                        time.sleep(self.hymn_delay * 60)
                        self.is_video = True
                        self.was_no_hymn = False
                    else:
                        self.new_record_terminal_tree(f'Variable_flag_hymn_is_{self.flag_hymn}_and_today_is_not_Monday')
                        self.is_video = True
                        self.was_no_hymn = False
                else:
                    self.new_record_terminal_tree(f'Variable_flag_hymn_is_{self.flag_hymn}')
                    self.is_video = True
                    self.was_no_hymn = False

            if self.is_video:
                if self.flag_video == 1:
                    if self.was_black_screen:
                        keyboard.press_and_release('F11')
                        time.sleep(self.delay)
                        keyboard.press('alt')
                        time.sleep(self.delay)
                        keyboard.press_and_release('F4')
                        time.sleep(self.delay)
                        keyboard.release('alt')
                        self.was_black_screen = False
                    self.day_of_the_week = int(datetime.datetime.weekday(datetime.datetime.now()))
                    if self.day_of_the_week == 0:
                        if self.monday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Monday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 1:
                        if self.tuesday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Tuesday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 2:
                        if self.wednesday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Wednesday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 3:
                        if self.thursday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Thursday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 4:
                        if self.friday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Friday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 5:
                        if self.saturday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Saturday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                    elif self.day_of_the_week == 6:
                        if self.sunday == 1:
                            self.play_videos = True
                            self.is_video = False
                        else:
                            self.new_record_terminal_tree('No_playing_on_this_Sunday')
                            self.is_video = False
                            self.reload_file = True
                            time.sleep(61)
                else:
                    self.new_record_terminal_tree(f'Flag_video_is_{self.flag_video}')
                    time.sleep(61)
                    self.is_video = False
                    self.reload_file = True

            while self.play_videos:
                for i in range(len(self.videos)):
                    self.new_record_terminal_tree("Starting_video")
                    os.startfile(self.videos[i])
                    mouse.move(self.screen_width // 2, self.screen_height // 2)
                    if self.double_click_var == 1:
                        time.sleep(5)
                        mouse.double_click()
                    time.sleep(self.videos_delay[i] * 60)
                    self.timenow = str(datetime.datetime.now()).split(' ')[1]
                    self.new_record_terminal_tree(f'Time-->{str(self.timenow[:2])}:{str(self.timenow[3:5])}')
                    if int(self.timenow[:2]) >= 17 and int(self.timenow[3:5]) >= 00:
                        self.new_record_terminal_tree('Day_ended')
                        self.play_videos = False
                        self.reload_file = True
                        break

            if self.reload_file:
                self.load_data()
                self.was_black_screen = True
                os.startfile('black_screen.jpg')
                time.sleep(15)
                keyboard.press_and_release('F11')
                time.sleep(5)
                mouse.move(self.screen_width + 100, self.screen_height // 2)

            time.sleep(1)

if __name__ == '__main__':
    app = MY_WINDOW()
