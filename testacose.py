import pickle
import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import datetime
import numpy as np
from tkinter import *


ABSPATH=os.path.dirname(os.path.abspath(__file__))

def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

if(isWindows()): 
    PATHSTATSFOLDER= ABSPATH+"\\output\\logbook" #path per windows
else: PATHSTATSFOLDER= ABSPATH+"/output/logbook/" #path per unix
  

def genstockdf():
        stockdf=[]
        stocknames=[] 
        i=0
        for stock in os.listdir(PATHCSVFOLDER):
            if(stock!='.DS_Store'):
                stocknames.append(stock[:-4])
                path=os.path.join(PATHCSVFOLDER, stocknames[i]+'.csv')
                df=pd.read_csv(path,usecols=["Date","Open","High","Low","Close","Adj Close","Volume"])
                stockdf.append(df)
                i+=1
        return (stockdf,stocknames)

def set_tkloadlogbook(dumpnames):
    
    win = Tk()
    win.title("Logbook Disponibili")
    # win.geometry("700x250")
    checkboxes = {}

    def genlist_to_load():
        global LOAD
        if (len(LOAD)==0):
            for box in checkboxes:
                LOAD.append(box.var.get())
            print('button',LOAD)
            win.destroy()
        elif (len(LOAD)==len(checkboxes)):
            LOAD=[]
            for box in checkboxes:
                LOAD.append(box.var.get())
            print('button',LOAD)
            win.destroy()
        else: print("impossibile")


    def ShowCheckBoxes(dumpnames):
        Cbcolumn = 0
        Cbrow = 4
        Chkcount = 0

        for Checkbox in range(len(dumpnames)):
            name = dumpnames[Checkbox]
            indpref = Checkbox
            current_var = IntVar()
            current_box = Checkbutton(win, text=name, variable=current_var)
            current_box.var = current_var
            current_box.grid(row=Cbrow, column=Cbcolumn)
            checkboxes[current_box] = indpref  # so checkbutton object is the key and value is string
            if Cbcolumn == 0:
                Cbcolumn = 0
                Cbrow += 1
            else:
                Cbcolumn += 1
            Chkcount += 1

    Button(win, text='PLOT FILE SELEZIONATO', command=genlist_to_load).grid(row=1000, column=0, columnspan=3)
    ShowCheckBoxes(dumpnames)
    win.mainloop()

def gendumpnames():
        dumpnames=[]
        pattern="*.*"
        i=0
        for dump in os.listdir(PATHSTATSFOLDER):
            if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
                dumpnames.append(dump[:-5])
                i+=1
        return dumpnames

stockdf,stocknames= genstockdf()
MAXTIME=24

def graficoriskyield(minrisk,minyield,maxrisk,maxyield,avgrisk,avgyield,stdrisk,stdyield,filename="File"):
    plt.style.use("ggplot")
    # fig, ((ax1,ax2,ax3,ax4)) = plt.subplots(nrows=4, ncols=1, sharex=True,figsize=(10, 8))
    fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(15, 6))

    maxtime=int(filename[filename.find("MAXTIME=")+8:filename.find("_TOURNPARAM")])
    date = pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(maxrisk))
    
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.8f}'))
    
    fig.suptitle(f"{filename}")
    
    ax1.plot(date,stdyield,label=f"Y std: {np.std(stdyield)}",color="black")
    ax1.plot(date,minyield,label=f"Y min: {min(minyield)}",color="blue")
    ax1.plot(date,avgyield,label=f"Y avg: {np.mean(avgyield)}",color="green")
    ax1.plot(date,maxyield,label=f"Y max: {max(maxyield)}",color="red")
    ax1.set_title(f"Yield")
    ax1.set_ylabel("Yield")
    ax1.legend()

    ax2.plot(date,stdrisk,label=f"R std: {np.std(stdrisk)}",color="black")
    ax2.plot(date,minrisk,label=f"R min: {min(minrisk)}",color="blue")
    ax2.plot(date,avgrisk,label=f"R avg: {np.mean(avgrisk)}",color="green")
    ax2.plot(date,maxrisk,label=f"R max: {max(maxrisk)}",color="red")
    ax2.set_title(f"Risk")
    ax2.set_ylabel("% Rischio")
    ax2.set_xlabel(f'Data\n Dal {stockdf[0]["Date"][0]} al {stockdf[0]["Date"][maxtime-1]} maxtime:{maxtime}')
    ax2.legend()
    
    fig.legend()
    plt.gcf().autofmt_xdate()
    plt.show()   

# with open('logb.txt', 'w') as logb:
#     for i in range(len(stats)):
#         print(stats[i],file=logb)


def plotlogbook(path):

    filename=path[len(PATHSTATSFOLDER)+1:-5]
    stats=pickle.load(open(path,"rb"))

    listminrisk=[]
    listminyield=[]

    listmaxrisk=[]
    listmaxyield=[]

    listavgrisk=[]
    listavgyield=[]

    liststdrisk=[]
    liststdyield=[]

    for logb in stats:
        for stat in logb:

            minrisk=stat["min"][0]
            minyield=stat["min"][1]
            listminrisk.append(minrisk)
            listminyield.append(minyield)

            maxrisk=stat["max"][0]
            maxyield=stat["max"][1]
            listmaxrisk.append(maxrisk)
            listmaxyield.append(maxyield)

            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)

            stdrisk=stat["std"][0]
            stdyield=stat["std"][1]
            liststdrisk.append(stdrisk)
            liststdyield.append(stdyield)

    graficoriskyield(listminrisk,listminyield,listmaxrisk,listmaxyield,listavgrisk,listavgyield,liststdrisk,liststdyield,filename)



# if(len(listminrisk)==len(listminyield)==len(listmaxrisk)==len(listmaxyield)==len(listavgrisk)==len(listavgyield)==len(liststdrisk)==len(liststdyield)):
#     print(f'lunghezza logbook: {len(listmaxyield)}')

LOAD=[]
dumpnames=gendumpnames()
set_tkloadlogbook(dumpnames)
for i in range(len(LOAD)):
    if LOAD[i]==1:
        path=os.path.join(PATHSTATSFOLDER, dumpnames[i]+'.dump')
        plotlogbook(path)
