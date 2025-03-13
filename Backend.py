import numpy as np
import pandas as pd
import os
import datetime as dt

dr = {}
dr_new = {}

cwd = os.getcwd()
#keys = ['DOC', 'EXT', 'FIG', 'MAT', 'RAW', 'REP', 'STC', 'VID']

keys_new = ['DATA', 'CHANGE_LOG', 'SETTINGS']

#dr.update({k: '%s/%s/' % (cwd, k) for k in keys})
dr_new.update({k: '%s/%s/' % (cwd, k) for k in keys_new})
#for k in dr:
#    os.makedirs(dr[k], exist_ok=True)

for k in dr_new:
    os.makedirs(dr_new[k], exist_ok=True)



class Backend():
    def makeDf(self, lst):
        columns = 'Activity', 'From', 'To', 'Office', 'Location', 'Notes'
        a = pd.DataFrame(lst, columns=columns)
        a['Duration'] = a['To'] - a['From']
        return a

    def updateSaves(self, aa):
        if os.path.exists(dr_new['DATA'] + 'TimeSheet.csv'):
            d_ = self.loadCsv(dr_new['DATA'] + 'TimeSheet.csv')
        else:
            d_ = pd.DataFrame(
                columns=['Activity', 'From', 'To', 'Office', 'Location', 'Notes', 'Duration'])
        d_ = pd.concat((d_, aa), ignore_index=True)
        self.saveCsv(d_, dr_new['DATA'] + 'TimeSheet.csv')
        self.saveCsv(d_, dr_new['CHANGE_LOG'] + dt.datetime.now().strftime('TimeSheet-%y%m%d-%H%M%S.csv'))

        return d_

    def loadCsv(self, fn):
        '''
            It will load the Activity data as a DataFrame using pandas
            fn: output file name + path
        '''
        return pd.read_csv(fn, index_col=0)

    def saveCsv(self, df, fn):
        '''
            It will save the DataFrame using pandas
            pd: DataFrame
            fn: output file name + path
        '''
        df.to_csv(fn)



    def openfile(self, path):
        file = open(path, 'r')
        s = file.read()
        file.close()
        return s.split(";")

    def getItem(self, path, action):
        if action == 'Activity':
            return self.getActivity(path)
        elif action == 'Location':
            return self.getLocation(path)

    def setItem(self, item, path, action):
        if action == 'Activity':
            print(action)
            self.setActivity(item, path)
        elif action == 'Location':
            self.setLocation(item, path)


    def getActivity(self,path):
        act = self.openfile(path+'Activity.txt')
        return act

    def savefile(self,path, data):
        file = open(path,'w')
        file.write(";".join(data))
        file.close()

    def setActivity(self, act, path):
        self.savefile(path+'Activity.txt', act)

    def getLocation(self,path):
        loc = self.openfile(path+'Location.txt')
        return loc

    def setLocation(self, loc, path):
        self.savefile(path+'Location.txt', loc)

    def saveNotes(self, notes):
        print(1)
