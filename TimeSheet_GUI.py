from tkinter import *
from tkinter import font as tkfont
import pandas as pd
#from tksheet import Sheet
import numpy as np
import tkinter as tk
import os
import sys
import socket
import platform
import datetime as dt
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

import time
import threading
import warnings



dr = {}
dr_new = {}

cwd = os.getcwd()
keys = ['DOC', 'EXT', 'FIG', 'MAT', 'RAW', 'REP', 'STC', 'VID']

keys_new = ['DATA', 'CHANGE_LOG', 'SETTINGS']

dr.update({k: '%s/%s/' % (cwd, k) for k in keys})
dr_new.update({k: '%s/%s/' % (cwd, k) for k in keys_new})
for k in dr:
    os.makedirs(dr[k], exist_ok=True)

for k in dr_new:
    os.makedirs(dr_new[k], exist_ok=True)


def make_df(lst):
    columns = 'Activity', 'From', 'To'
    a = pd.DataFrame(lst, columns=columns)
    a['Duration'] = a['To'] - a['From']
    return a


def update_saves(aa):
    if os.path.exists(dr_new['DATA'] + 'TimeSheet.csv'):
        d_ = load_csv(dr_new['DATA'] + 'TimeSheet.csv')
    else:
        d_ = pd.DataFrame(
            columns=['Activity', 'From', 'To', 'Office', 'Location', 'Notes', 'Duration'])
    d_ = pd.concat((d_, aa), ignore_index=True)
    save_csv(d_, dr_new['DATA'] + 'TimeSheet.csv')
    save_csv(d_, dr_new['CHANGE_LOG'] + dt.datetime.now().strftime('TimeSheet-%y%m%d-%H%M%S.csv'))

    return d_


def load_csv(fn):
    '''
        It will load the Activity data as a DataFrame using pandas
        fn: output file name + path
    '''
    return pd.read_csv(fn, index_col=0)


def save_csv(df, fn):
    '''
        It will save the DataFrame using pandas
        pd: DataFrame
        fn: output file name + path
    '''
    df.to_csv(fn)


class My_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Timer, ManualEntry, EditEntry, Settings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        print(page_name)
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        def refresh():
            table_tail(self, 3)

        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to....", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        widget_Tab(self, controller)

        button = tk.Button(self, text="Refresh", command=refresh)
        button.grid(row=2, column=0, sticky='w')
        table_tail(self, 3)


def table_tail(self, position, edit=False, ind=-3):
    table = tk.Frame(master=self, bg='blue')
    table.grid(row=position, column=0, padx='0', pady='5', sticky='w')
    if edit:
        df = load_csv(dr_new['DATA'] + 'TimeSheet.csv').loc[ind - 2:ind + 2]
    else:
        df = load_csv(dr_new['DATA'] + 'TimeSheet.csv').tail()
    arr = df.to_numpy()
    col = list(df.columns)

    for i in range(len(col)):
        e = tk.Label(table, text=col[i])
        e.grid(row=3, column=i, sticky='nsew')
    for i in range(5):
        for j in range(len(col)):
            e = tk.Label(table, text=str(arr[i, j]))
            e.grid(row=i + 4, column=j, sticky='nsew')


class Timer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to...." + pages[1], font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        ### ------------ Tab widget --------------

        widget_Tab(self, controller)

        ### --------- Timer Loops ------------------
        Activity = ['Working', 'Sleeping', 'Drinks', 'Refresh', 'Discussion']
        Office = ['d-fine Office', 'Home office', 'Client office']
        Location = ['Hamburg', 'Frankfurt']

        def loop_1():
            while button[0]['text'] == 'Stop':
                date2[0].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[0].get()))[7:-7])
                time.sleep(1)

        def loop_2():
            while button[1]['text'] == 'Stop':
                date2[1].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[1].get()))[7:-7])
                time.sleep(1)

        def loop_3():
            while button[2]['text'] == 'Stop':
                date2[2].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[2].get()))[7:-7])
                time.sleep(1)

        def start_click_1():
            '''
            Function for automatic time logging
            '''
            if button[0]['text'] == 'Start':

                date1[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                date2[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[0].config(text='Elapsed Time')
                button[0].config(text='Stop')

                threading.Thread(target=loop_1).start()

            else:
                date2[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[0].config(text='To')
                button[0].config(text='Start')

                F = pd.to_datetime(date1[0].get())
                T = pd.to_datetime(date2[0].get())

                date2[0].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[0].get()))[7:-7])
                date1[0].set(' ')
                aa = make_df([[act[0].get(), F, T]])

                d = update_saves(aa)
                table_tail(self, 5)

        def start_click_2():
            '''
            Function for automatic time logging
            '''
            if button[1]['text'] == 'Start':

                date1[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                date2[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[1].config(text='Elapsed Time')
                button[1].config(text='Stop')

                threading.Thread(target=loop_2).start()

            else:
                date2[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[1].config(text='To')
                button[1].config(text='Start')

                F = pd.to_datetime(date1[1].get())
                T = pd.to_datetime(date2[1].get())

                date2[1].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[1].get()))[7:-7])
                date1[1].set(' ')
                aa = make_df([[act[1].get(), F, T]])

                d = update_saves(aa)
                table_tail(self, 5)

        def start_click_3():
            '''
            Function for automatic time logging
            '''
            if button[2]['text'] == 'Start':

                date1[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                date2[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[2].config(text='Elapsed Time')
                button[2].config(text='Stop')

                threading.Thread(target=loop_3).start()

            else:
                date2[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                label2[2].config(text='To')
                button[2].config(text='Start')

                F = pd.to_datetime(date1[2].get())
                T = pd.to_datetime(date2[2].get())

                date2[2].set(str(dt.datetime.today() -
                                 pd.to_datetime(date1[2].get()))[7:-7])
                date1[2].set(' ')
                aa = make_df([[act[2].get(), F, T]])

                d = update_saves(aa)
                table_tail(self, 5)

        rahmen = {}
        label = {}
        w = {}
        button = {}
        label1 = {}
        label2 = {}
        entry1 = {}
        entry2 = {}
        act = {}
        date1 = {}
        date2 = {}
        click_commands = [start_click_1, start_click_2, start_click_3]

        def createTimer(enum):

            rahmen[enum] = tk.Frame(master=self, bg='magenta')
            rahmen[enum].grid(row=2 + enum, column=0, padx='0', pady='5', sticky='w')

            label[enum] = tk.Label(rahmen[enum], text="Activity")
            label[enum].pack(side='left')

            OPTIONS = ["Jan", "Feb", "Mar"]  # etc

            act[enum] = tk.StringVar(self)
            act[enum].set(OPTIONS[0])
            w[enum] = tk.OptionMenu(rahmen[enum], act[enum], *OPTIONS)
            w[enum].pack(side='left')
            button[enum] = tk.Button(rahmen[enum], text="Start", command=click_commands[enum])
            button[enum].pack(side='left')
            label1[enum] = tk.Label(rahmen[enum], text="From")
            label1[enum].pack(side='left')
            date1[enum] = tk.StringVar()
            entry1[enum] = tk.Entry(rahmen[enum], textvariable=date1[enum], width=10)
            date1[enum].set("Default")
            entry1[enum].pack(side='left')

            label2[enum] = tk.Label(rahmen[enum], text="To")
            label2[enum].pack(side='left')

            date2[enum] = tk.StringVar()
            entry2[enum] = tk.Entry(rahmen[enum], textvariable=date2[enum], width=10)
            date2[enum].set("Default")
            entry2[enum].pack(side='left')

        createTimer(0)
        createTimer(1)
        createTimer(2)
        table_tail(self, 5)

        # -------------------- Display --------------------


class ManualEntry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to...." + pages[2], font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        widget_Tab(self, controller)
        act, date1, date2 = tk.StringVar(self), tk.StringVar(self), tk.StringVar(self)

        def click_manual():
            F = pd.to_datetime(date1.get())
            T = pd.to_datetime(date2.get())

            aa = make_df([[act.get(), F, T]])

            d = update_saves(aa)
            table_tail(self, 3)

        def createManualTimer():
            rahmen = tk.Frame(master=self, bg='magenta')
            rahmen.grid(row=2, column=0, padx='0', pady='5', sticky='w')

            label = tk.Label(rahmen, text="Activity")
            label.pack(side='left')

            OPTIONS = ["Jan", "Feb", "Mar"]  # etc

            act.set(OPTIONS[0])
            w = tk.OptionMenu(rahmen, act, *OPTIONS)
            w.pack(side='left')
            button = tk.Button(rahmen, text="Enter", command=click_manual)
            button.pack(side='left')
            label1 = tk.Label(rahmen, text="From")
            label1.pack(side='left')
            entry1 = tk.Entry(rahmen, textvariable=date1, width=10)
            date1.set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            entry1.pack(side='left')

            label2 = tk.Label(rahmen, text="To")
            label2.pack(side='left')

            entry2 = tk.Entry(rahmen, textvariable=date2, width=10)
            date2.set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            entry2.pack(side='left')

        createManualTimer()


def widget_Tab(frame, controller):
    rahmen1 = tk.Frame(master=frame, bg='magenta')
    rahmen1.grid(row=1, column=0, padx='0', pady='5', sticky='w')

    button1 = tk.Button(rahmen1, text="Start Page",
                        command=lambda: controller.show_frame("StartPage"))
    button1.pack(side='left')

    button2 = tk.Button(rahmen1, text="Timer",
                        command=lambda: controller.show_frame("Timer"))
    button2.pack(side='left')

    button3 = tk.Button(rahmen1, text="Manual Entry",
                        command=lambda: controller.show_frame("ManualEntry"))
    button3.pack(side='left')

    button4 = tk.Button(rahmen1, text="Edit Entry",
                        command=lambda: controller.show_frame("EditEntry"))
    button4.pack(side='left')

    button5 = tk.Button(rahmen1, text="Settings",
                        command=lambda: controller.show_frame("Settings"))
    button5.pack(side='left')


class EditEntry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to...." + pages[3], font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        widget_Tab(self, controller)
        act, date1, date2, index = tk.StringVar(self), tk.StringVar(self), tk.StringVar(self), tk.StringVar(self)

        def update_edit_saves(df):
            d_ = load_csv(dr_new['DATA'] + 'TimeSheet.csv')
            ind = int(index.get())
            d_.at[ind, 'Activity'] = act.get()
            d_.at[ind, 'To'] = date1.get()
            d_.at[ind, 'From'] = date2.get()
            d_.at[ind, 'Duration'] = pd.to_datetime(date2.get()) - pd.to_datetime(date1.get())

            save_csv(d_, dr_new['DATA'] + 'TimeSheet.csv')
            save_csv(d_, dr_new['CHANGE_LOG'] + dt.datetime.now().strftime('TimeSheet-%y%m%d-%H%M%S.csv'))

        def click_edit():
            F = pd.to_datetime(date1.get())
            T = pd.to_datetime(date2.get())
            aa = make_df([[act.get(), F, T]])
            d = update_edit_saves(aa)
            table_tail(self, 3, True, int(index.get()))

        def click_del():
            print(0)

        def set_edit(self):
            if index.get() != 'Index':
                d_ = load_csv(dr_new['DATA'] + 'TimeSheet.csv')
                ind = int(index.get())
                print(ind)
                act.set(d_['Activity'].to_numpy()[ind])
                date1.set(d_['From'].to_numpy()[ind])
                date2.set(d_['To'].to_numpy()[ind])

        def createEdit():
            rahmen = tk.Frame(master=self, bg='magenta')
            rahmen.grid(row=2, column=0, padx='0', pady='5', sticky='w')
            d_ = load_csv(dr_new['DATA'] + 'TimeSheet.csv')
            OPTIONS_INDEX = list(range(len(d_['Activity'].to_numpy())))
            index.set('Index')
            index_ent = tk.OptionMenu(rahmen, index, *OPTIONS_INDEX, command=set_edit)
            index_ent.pack(side='left')
            label = tk.Label(rahmen, text="Activity")
            label.pack(side='left')
            OPTIONS = ["Jan", "Feb", "Mar"]  # etc
            act.set(OPTIONS[0])
            w = tk.OptionMenu(rahmen, act, *OPTIONS)
            w.pack(side='left')
            button = tk.Button(rahmen, text="Enter", command=click_edit)
            button.pack(side='left')
            label1 = tk.Label(rahmen, text="From")
            label1.pack(side='left')
            entry1 = tk.Entry(rahmen, textvariable=date1, width=10)
            entry1.pack(side='left')
            label2 = tk.Label(rahmen, text="To")
            label2.pack(side='left')
            entry2 = tk.Entry(rahmen, textvariable=date2, width=10)
            entry2.pack(side='left')

        def deleteEntry():
            rahmen = tk.Frame(master=self, bg='magenta')
            rahmen.grid(row=3, column=0, padx='0', pady='5', sticky='w')
            d_ = load_csv(dr_new['DATA'] + 'TimeSheet.csv')
            OPTIONS_INDEX = list(range(len(d_['Activity'].to_numpy())))
            index.set('Index')
            index_ent = tk.OptionMenu(rahmen, index, *OPTIONS_INDEX, command=set_edit)
            index_ent.pack(side='left')
            button = tk.Button(rahmen, text="Delete", command=click_del)
            button.pack(side='left')

        createEdit()
        deleteEntry()


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to...." + pages[4], font=controller.title_font)
        label.grid(row=0, column=0, columnspan=2)

        widget_Tab(self, controller)


pages = ['StartPage', 'Timer', 'ManualEntry', 'EditEntry', 'Settings']

if __name__ == "__main__":
    app = My_GUI()
    app.mainloop()