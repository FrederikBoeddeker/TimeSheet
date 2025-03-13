from tkinter import *
from tkinter import font as tkfont
import pandas as pd
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
from Backend import Backend

back = Backend()

OFFICE = ['d-fine Office', 'Home office', 'Client office']

dr = {}
cwd = os.getcwd()
keys = ['DATA', 'CHANGE_LOG', 'SETTINGS']
dr.update({k: '%s/%s/' % (cwd, k) for k in keys})
for k in dr:
    os.makedirs(dr[k], exist_ok=True)


class My_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.initial()

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

    def table_tail(self, frame, position, edit=False, ind=-3):
        table = tk.Frame(master=frame, bg='blue')
        table.grid(row=position, column=0, padx='0', pady='5', sticky='w')
        if edit:
            df = back.loadCsv(dr['DATA'] + 'TimeSheet.csv')
            if ind < 2:
                ind= 2
            elif ind > df.shape[0]-2:
                ind = df.shape[0]-2
            df = df.loc[ind - 2:ind + 2]
        else:
            df = back.loadCsv(dr['DATA'] + 'TimeSheet.csv').tail()
        col = ['Index']+df.columns.tolist()
        df['Index'] = df.index
        arr = df[col].to_numpy()
        for i in range(len(col)):
            e = tk.Label(table, text=col[i])
            e.grid(row=3, column=i, sticky='nsew')
        for i in range(5):
            for j in range(len(col)):
                e = tk.Label(table, text=str(arr[i, j]))
                e.grid(row=i + 4, column=j, sticky='nsew')

    def widget_Tab(self, frame, row):
        rahmen1 = tk.Frame(master=frame, bg='magenta')
        rahmen1.grid(row=row, column=0, padx='0', pady='5', sticky='w')

        button1 = tk.Button(rahmen1, text="Start Page",
                            command=lambda: self.show_frame("StartPage"))
        button1.pack(side='left')

        button2 = tk.Button(rahmen1, text="Timer",
                            command=lambda: self.show_frame("Timer"))
        button2.pack(side='left')

        button3 = tk.Button(rahmen1, text="Manual Entry",
                            command=lambda: self.show_frame("ManualEntry"))
        button3.pack(side='left')

        button4 = tk.Button(rahmen1, text="Edit Entry",
                            command=lambda: self.show_frame("EditEntry"))
        button4.pack(side='left')

        button5 = tk.Button(rahmen1, text="Settings",
                            command=lambda: self.show_frame("Settings"))
        button5.pack(side='left')

    def initial(self):
        try:
            back.getActivity(dr['SETTINGS'])
        except:
            back.setActivity(['Working'], dr['SETTINGS'])

        try:
            back.getLocation(dr['SETTINGS'])
        except:
            back.setLocation(['Hamburg'], dr['SETTINGS'])


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.rows = 0
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome to....", font=controller.title_font)
        label.grid(row=self.rows, column=0, columnspan=2)
        self.rows+=1

        controller.widget_Tab( self, self.rows)
        self.rows +=1

        button = tk.Button(self, text="Refresh", command=self.refresh)
        button.grid(row=self.rows, column=0, sticky='w')
        self.rows += 1
        controller.table_tail(self, self.rows)

    def refresh(self):
        self.controller.table_tail(self, self.rows)



class Timer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Welcome to...." + pages[1], font=controller.title_font)
        label.grid(row=1, column=0, columnspan=2)

        ### ------------ Tab widget --------------

        controller.widget_Tab(self, 2)

        ### --------- Timer Loops ------------------
        #Activity = ['Working', 'Sleeping', 'Drinks', 'Refresh', 'Discussion']

        self.activ = {}
        self.From = {}
        self.To = {}
        self.Loca = {}
        self.Office = {}
        self.notes = {}
        clickCommands = [self.start_click_1, self.start_click_2, self.start_click_3]

        self.createTimer(0, clickCommands)
        self.createTimer(1, clickCommands)
        self.createTimer(2, clickCommands)
        controller.table_tail(self, 5)

    def loop_1(self, button):
        while button['text'] == 'Stop':
            self.To[0].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[0].get()))[7:-7])
            time.sleep(1)

    def loop_2(self, button):
        while button['text'] == 'Stop':
            self.To[1].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[1].get()))[7:-7])
            time.sleep(1)

    def loop_3(self, button):
        while button['text'] == 'Stop':
            self.To[2].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[2].get()))[7:-7])
            time.sleep(1)

    def start_click_1(self,button,label2):
        '''
        Function for automatic time logging
        '''
        if button['text'] == 'Start':

            self.From[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.To[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='Elapsed Time')
            button.config(text='Stop')

            threading.Thread(target=lambda:self.loop_1(button)).start()

        else:
            self.To[0].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='To')
            button.config(text='Start')

            df = back.makeDf([[self.activ[0].get(), pd.to_datetime(self.From[0].get()), pd.to_datetime(self.To[0].get()),
                               self.Office[0].get(), self.Loca[0].get(), self.notes[0].get()]])

            self.To[0].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[0].get()))[7:-7])
            self.From[0].set(' ')

            d = back.updateSaves(df)
            self.controller.table_tail(self, 5)

    def start_click_2(self, button, label2):
        '''
        Function for automatic time logging
        '''
        if button['text'] == 'Start':

            self.From[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.To[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='Elapsed Time')
            button.config(text='Stop')

            threading.Thread(target=lambda:self.loop_2(button)).start()

        else:
            self.To[1].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='To')
            button.config(text='Start')

            df = back.makeDf([[self.activ[1].get(), pd.to_datetime(self.From[1].get()), pd.to_datetime(self.To[1].get()),
                               self.Office[1].get(), self.Loca[1].get(), self.notes[1].get()]])
            self.To[1].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[1].get()))[7:-7])
            self.From[1].set(' ')
            d = back.updateSaves(df)
            self.controller.table_tail(self, 5)

    def start_click_3(self, button, label2):
        '''
        Function for automatic time logging
        '''
        if button['text'] == 'Start':

            self.From[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            self.To[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='Elapsed Time')
            button.config(text='Stop')

            threading.Thread(target=lambda:self.loop_3(button)).start()

        else:
            self.To[2].set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            label2.config(text='To')
            button.config(text='Start')

            df = back.makeDf([[self.activ[2].get(), pd.to_datetime(self.From[2].get()), pd.to_datetime(self.To[2].get()),
                               self.Office[2].get(), self.Loca[2].get(), self.notes[2].get()]])

            self.To[2].set(str(dt.datetime.today() -
                               pd.to_datetime(self.From[2].get()))[7:-7])
            self.From[2].set(' ')

            d = back.updateSaves(df)
            self.controller.table_tail(self, 5)

    def clickNotes(self):
        print(1)

    def createTimer(self, enum, clickCommands):

        rahmen = tk.Frame(master=self, bg='magenta')
        rahmen.grid(row=3 + enum, column=0, padx='0', pady='5', sticky='w')
        button = tk.Button(rahmen, text="Start", command=lambda: clickCommands[enum](button, label2))
        button.pack(side='left')
        #label = tk.Label(rahmen, text="Activity")
        #label.pack(side='left')

        OPTIONS = back.getItem(dr['SETTINGS'], 'Activity')  # etc

        self.activ[enum] = tk.StringVar()
        self.activ[enum].set(OPTIONS[0])
        w = tk.OptionMenu(rahmen, self.activ[enum], *OPTIONS)
        w.pack(side='left')


        label1 = tk.Label(rahmen, text="From")
        label1.pack(side='left')
        self.From[enum] = tk.StringVar()
        self.From[enum].set("Default")
        entry1 = tk.Entry(rahmen, textvariable=self.From[enum], width=10)
        entry1.pack(side='left')

        label2 = tk.Label(rahmen, text="To")
        label2.pack(side='left')

        self.To[enum] = tk.StringVar()
        self.To[enum].set("Default")
        entry2 = tk.Entry(rahmen, textvariable=self.To[enum], width=10)
        entry2.pack(side='left')

        LOCATIONS = back.getItem(dr['SETTINGS'], 'Location')
        self.Loca[enum] = tk.StringVar()
        self.Loca[enum].set(LOCATIONS[0])
        self.Office[enum] = tk.StringVar()
        self.Office[enum].set(OFFICE[0])
        #label3 = tk.Label(rahmen, text='Location')
        #label3.pack(side='left')
        w1 = tk.OptionMenu(rahmen, self.Office[enum], *OFFICE)
        w1.pack(side='left')

        w2 = tk.OptionMenu(rahmen, self.Loca[enum], *LOCATIONS)
        w2.pack(side='left')

        self.notes[enum] = StringVar()
        self.notes[enum].set('test string')
        self.notebutton = tk.Button(rahmen, text="Entry Notes", command=lambda:self.clickNotes(enum))
        self.notebutton.pack(side='left')

    def clickNotes(self,enum):
        #print(self.notes[enum].get())
        self.w=popupWindow(self.parent, self.notes[enum])
        self.notebutton["state"] = "disabled"
        self.parent.wait_window(self.w.top)
        self.notebutton["state"] = "normal"

    def entryValue(self):
        return self.w.value


class popupWindow(object):
    def __init__(self,parent, note):
        top=self.top=Toplevel(parent)
        top.geometry("350x200")
        self.l=Label(top,text="Entry Note")
        self.l.pack()
        self.e=tk.Text(top, width=10, height=8)
        self.e.insert(INSERT,note.get())
        self.e.pack(fill=BOTH, expand=1)
        self.b=Button(top,text='Ok',command=lambda:self.cleanup(note))
        self.b.pack()
    def cleanup(self, note):
        self.value=self.e.get("1.0", END)
        note.set(self.e.get("1.0", END))
        back.saveNotes(self.value)
        self.top.destroy()


class ManualEntry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.activ = tk.StringVar()
        self.From = tk.StringVar()
        self.To = tk.StringVar()
        self.Office = tk.StringVar()
        self.Loca = tk.StringVar()
        self.notes = tk.StringVar()

        label = tk.Label(self, text="Welcome to...." + pages[2], font=controller.title_font)
        label.grid(row=0, column=1, columnspan=2)

        controller.widget_Tab( self,2)

        self.createManualTimer()

    def click_manual(self):
        df = back.makeDf([[self.activ.get(), pd.to_datetime(self.From.get()), pd.to_datetime(self.To.get()),
                           self.Office.get(), self.Loca.get(), self.notes.get()]])

        d = back.updateSaves(df)
        self.controller.table_tail(self, 3)

    def createManualTimer(self):
        rahmen = tk.Frame(master=self, bg='magenta')
        rahmen.grid(row=3, column=0, padx='0', pady='5', sticky='w')

        button = tk.Button(rahmen, text="Enter", command=self.click_manual)
        button.pack(side='left')
        OPTIONS = back.getItem(dr['SETTINGS'], 'Activity')
        LOCATION = back.getItem(dr['SETTINGS'], 'Location')

        self.activ.set(OPTIONS[0])
        w = tk.OptionMenu(rahmen, self.activ, *OPTIONS)
        w.pack(side='left')

        label1 = tk.Label(rahmen, text="From")
        label1.pack(side='left')
        entry1 = tk.Entry(rahmen, textvariable=self.From, width=10)
        self.From.set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        entry1.pack(side='left')

        label2 = tk.Label(rahmen, text="To")
        label2.pack(side='left')

        entry2 = tk.Entry(rahmen, textvariable=self.To, width=10)
        self.To.set(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        entry2.pack(side='left')
        self.Loca.set(LOCATION[0])

        self.Office.set(OFFICE[0])
        w1 = tk.OptionMenu(rahmen, self.Office, *OFFICE)
        w1.pack(side='left')

        w2 = tk.OptionMenu(rahmen, self.Loca, *LOCATION)
        w2.pack(side='left')

        self.notes = StringVar()
        self.notes.set('test string')
        self.notebutton = tk.Button(rahmen, text="Entry Notes", command=lambda: self.clickNotes())
        self.notebutton.pack(side='left')

    def clickNotes(self):
        self.w=popupWindow(self.parent, self.notes)
        self.notebutton["state"] = "disabled"
        self.parent.wait_window(self.w.top)
        self.notebutton["state"] = "normal"

    def entryValue(self):
        return self.w.value



class EditEntry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #activ, From, To, index = tk.StringVar(self), tk.StringVar(self), tk.StringVar(self), tk.StringVar(self)

        self.activ = tk.StringVar()
        self.From = tk.StringVar()
        self.To = tk.StringVar()
        self.index = tk.StringVar()
        self.Office = tk.StringVar()
        self.Loca = tk.StringVar()
        self.notes = tk.StringVar()

        label = tk.Label(self, text="Welcome to...." + pages[3], font=controller.title_font)
        label.grid(row=1, column=0, columnspan=2)

        controller.widget_Tab( self,2)
        self.createEdit()
        self.deleteEntry()

    def getINDEX(self):
        d_ = back.loadCsv(dr['DATA'] + 'TimeSheet.csv')
        return list(range(len(d_['Activity'].to_numpy())))

    def refreshINDEX(self, w):
        w['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        for idx in self.getINDEX():
            w['menu'].add_command(label=idx, command=tk._setit(self.index, idx))


    def updateEditSaves(self):
        d_ = back.loadCsv(dr['DATA'] + 'TimeSheet.csv')
        ind = int(self.index.get())
        d_.at[ind, 'Activity'] = self.activ.get()
        d_.at[ind, 'To'] = self.To.get()
        d_.at[ind, 'From'] = self.From.get()
        d_.at[ind, 'Duration'] = pd.to_datetime(self.To.get()) - pd.to_datetime(self.From.get())

        back.saveCsv(d_, dr['DATA'] + 'TimeSheet.csv')
        back.saveCsv(d_, dr['CHANGE_LOG'] + dt.datetime.now().strftime('TimeSheet-%y%m%d-%H%M%S.csv'))

    def clickEdit(self, w):
        F = pd.to_datetime(self.From.get())
        T = pd.to_datetime(self.To.get())
        list = [self.activ.get(), F, T]
        self.updateEditSaves()
        self.refreshINDEX(w)
        self.controller.table_tail(self, 4, True, int(self.index.get()))

    def clickDel(self, w):
        print(0)
        if self.index.get() != 'Index':
            d_ = back.loadCsv(dr['DATA'] + 'TimeSheet.csv')
            idx = int(self.index.get())
            print(idx)
            d1_ = d_.drop(idx)
            d1_ = d1_.reset_index(drop=True)
            back.saveCsv(d1_, dr['DATA'] + 'TimeSheet.csv')
            back.saveCsv(d1_, dr['CHANGE_LOG'] + dt.datetime.now().strftime('TimeSheet-%y%m%d-%H%M%S.csv'))
            self.refreshINDEX(w)
            self.controller.table_tail(self, 4, True, int(idx))





    def createEdit(self):
        INDEX = self.getINDEX()

        OPTIONS = back.getItem(dr['SETTINGS'], 'Activity')
        LOCATION = back.getItem(dr['SETTINGS'], 'Location')

        rahmen = tk.Frame(master=self, bg='magenta')
        rahmen.grid(row=3, column=0, padx='0', pady='5', sticky='w')
        #index = dict('index')
        self.index.set('Index')
        button = tk.Button(rahmen, text="Enter", command=lambda: self.clickEdit(index_ent))
        button.pack(side='left')
        index_ent = tk.OptionMenu(rahmen, self.index, *INDEX, command=lambda x:self.setEdit())
        index_ent.pack(side='left')
        OPTIONS = ["Jan", "Feb", "Mar"]  # etc
        self.activ.set(OPTIONS[0])
        w = tk.OptionMenu(rahmen, self.activ, *OPTIONS)
        w.pack(side='left')

        label1 = tk.Label(rahmen, text="From")
        label1.pack(side='left')
        entry1 = tk.Entry(rahmen, textvariable=self.From, width=10)
        entry1.pack(side='left')
        label2 = tk.Label(rahmen, text="To")
        label2.pack(side='left')
        entry2 = tk.Entry(rahmen, textvariable=self.To, width=10)
        entry2.pack(side='left')
        self.Loca.set(LOCATION[0])

        self.Office.set(OFFICE[0])
        w1 = tk.OptionMenu(rahmen, self.Office, *OFFICE)
        w1.pack(side='left')

        w2 = tk.OptionMenu(rahmen, self.Loca, *LOCATION)
        w2.pack(side='left')

        self.notes = StringVar()
        self.notes.set('test string')
        self.notebutton = tk.Button(rahmen, text="Entry Notes", command=lambda: self.clickNotes())
        self.notebutton.pack(side='left')

    def clickNotes(self):
        self.w = popupWindow(self.parent, self.notes)
        self.notebutton["state"] = "disabled"
        self.parent.wait_window(self.w.top)
        self.notebutton["state"] = "normal"

    def entryValue(self):
        return self.w.value

    def setEdit(self):
        if self.index.get() != 'Index':
            d_ = back.loadCsv(dr['DATA'] + 'TimeSheet.csv')
            ind = int(self.index.get())
            self.activ.set(d_['Activity'].to_numpy()[ind])
            self.From.set(d_['From'].to_numpy()[ind])
            self.To.set(d_['To'].to_numpy()[ind])
            self.Office.set(d_['Office'].to_numpy()[ind])
            self.Loca.set(d_['Location'].to_numpy()[ind])
            self.notes.set(d_['Notes'].to_numpy()[ind])

    def deleteEntry(self):
        rahmen = tk.Frame(master=self, bg='magenta')
        rahmen.grid(row=4, column=0, padx='0', pady='5', sticky='w')

        self.index.set('Index')
        index_ent = tk.OptionMenu(rahmen, self.index, *self.getINDEX())
        index_ent.pack(side='left')
        button = tk.Button(rahmen, text="Delete", command=lambda:self.clickDel(index_ent))
        button.pack(side='left')




class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.loca

        header = tk.Frame(master=self, bg='blue')
        header.grid(row=0, column=0, padx='0', pady='5', sticky='w')


        label = tk.Label(self, text="Welcome to...." + pages[4], font=controller.title_font)
        label.grid(row=1, column=0, columnspan=2)

        controller.widget_Tab( self,2)

        action, text = tk.StringVar(self), tk.StringVar(self)
        self.createAdd(action, text)

    def clickAdd(self, action, text):
        item = back.getItem(dr['SETTINGS'], action.get())
        if text.get() in item:
            back.setItem(item, dr['SETTINGS'], action.get())
        else:
            back.setItem(item + [text.get()], dr['SETTINGS'], action.get())


    def clickDel(self, action, text):

        item = back.getItem(dr['SETTINGS'], action.get())
        try:
            item.remove(text.get())
        except:
            print('Error 101')
        back.setItem(item, dr['SETTINGS'], action.get())

    def createAdd(self, action, text):
        rahmen = tk.Frame(master=self, bg='magenta')
        rahmen.grid(row=3, column=0, padx='0', pady='5', sticky='w')
        ACTION = ['Activity', 'Location']
        ent = tk.OptionMenu(rahmen, action, *ACTION)
        ent.pack(side='left')
        entry1 = tk.Entry(rahmen, textvariable=text, width=10)
        entry1.pack(side='left')
        button1 = tk.Button(rahmen, text="Add", command=lambda: self.clickAdd(action, text) )
        button1.pack(side='left')
        button2 = tk.Button(rahmen, text="Delete", command=lambda: self.clickDel(action, text))
        button2.pack(side='left')

    def refresh(self):
        w['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        for idx in self.getINDEX():
            w['menu'].add_command(label=idx, command=tk._setit(self.index, idx))









pages = ['StartPage', 'Timer', 'ManualEntry', 'EditEntry', 'Settings']

if __name__ == "__main__":
    app = My_GUI()
    app.mainloop()