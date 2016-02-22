# -*- coding: utf-8 -*-

from jinja2 import Environment,FileSystemLoader
import pickle
import sys
import shutil
import os
import time

LOCKFILE = ".lockdata"

class INDEX(object):
    def GET(self):
        return "http://ip:port/enbquery\n"

class ENBQUERY(object):
    def __init__(self):
        self.filedata = 'enb_data.txt'
        self.backupdata = 'enb_backup.txt'
    def GET(self):
        env = Environment(loader=FileSystemLoader('./template'))
        try:
            fdata = open(self.filedata,'rb')
            getdata = pickle.load(fdata)
            fdata.close()
            #print len(getdata)
            tmpt = env.get_template('showlab.html')
            return tmpt.render(enbinfo=getdata,rows=range(len(getdata)),cols=range(len(getdata[0])))
        except AttributeError,e:
            tmpt = env.get_template('exception.html')
            return tmpt.render(reason=sys.exc_info)
    def POST(self,dt):
        data = self.transformdata(dt)
        #loaddata = []
        #singledata = []
        #print data.decode()
        #splitdata = data.split('&')
        #print splitdata
        #for elem in splitdata:
        #    splitelem = elem.split('=')
        #    singledata.append(splitelem[1])
        #    if splitelem[0] == 'Load':
        #        loaddata.append(singledata)
        #        singledata = []

        if os.path.exists(LOCKFILE): # conflict with others, should wait for a while
            return "Conflict with others, should wait for a while, refresh the page, then submit your data again"
        else: # not conflict with others
            os.mknod(LOCKFILE)
            shutil.copy(self.filedata,self.backupdata)
            output = open(self.filedata,'wb')
            pickle.dump(data,output)
            output.close()
            os.remove(LOCKFILE)
            return "submit successful"
    def transformdata(self,d):
        '''
        {'a':[],'b':[],...} --> [ [],[],... ]
        '''
        namelist = ['Identity','ProductName','Type','Location','IP','User','Status','Load']
        retdata = []
        singledata = []
        recordnb = len(d[namelist[0]])
        for i in range(recordnb):
            for eachname in namelist:
                singledata.append(d[eachname][i])
            retdata.append(singledata)
            singledata = []

        return retdata

class ROOT(object):
    def GET(self):
        return "Welcome\n"

if __name__ == "__main__":
    eq = ENBQUERY()

    # test 1
    #print eq.GET()

    # test 2
    a = {'Status': ['thanks%2Cbuddy%2Cthat%27s+should+be+ok', 'it%27s+a+nice+day', 'fantastic'], 'Load': ['', '', ''], 'IP': ['135.242.110.45', '135.242.110.93', '135.242.110.105'], 'ProductName': ['enb161', 'enb173', 'enb176'], 'User': ['lyz', 'cjy', ''], 'Type': ['', 'bcam2', 'eccm2'], 'Identity': ['1', '2', '3'], 'Location': ['at+f301', '', '']}
    print a
    print eq.transformdata(a)
