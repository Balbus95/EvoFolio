import pickle
import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from tkinter import *
from tkinter import ttk


ABSPATH=os.path.dirname(os.path.abspath(__file__))


def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

if(isWindows()): 
    PATHLOGBFOLDER= ABSPATH+"\\output\\logbook" #path per windows
else: PATHLOGBFOLDER= ABSPATH+"/output/logbook" #path per unix

  
def genstockdf():
        stockdf=[]
        stocknames=[] 
        pattern="*.csv"
        i=0
        for stock in os.listdir(PATHCSVFOLDER):
            if(stock!='.DS_Store' and fnmatch.fnmatch(stock, pattern)):
                stocknames.append(stock[:-4])
                path=os.path.join(PATHCSVFOLDER, stocknames[i]+'.csv')
                df=pd.read_csv(path,usecols=["Date","Open","High","Low","Close","Adj Close","Volume"])
                stockdf.append(df)
                i+=1
        return (stockdf,stocknames)

def gendumpnames():
        
    def lensort(filename):
        return len(filename[:filename.find("_MU")])

    dumpnames=[]
    pattern="*.dump"
    i=0
    for dump in os.listdir(PATHLOGBFOLDER):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])
            i+=1
    dumpnames.sort(key=lensort)
    return dumpnames

def tkloadlogbook(dumpnames):
  
    win = Tk()
    win.title("Logbook Disponibili")
    win.geometry("600x80")

    def closewin():
        win.destroy()

    def funprov(event):
        path=os.path.join(PATHLOGBFOLDER, file.get()+'.dump')
        plotlogbook(path)

    file=StringVar()
    file_combobox = ttk.Combobox(win, textvariable=file)
    file_combobox['values']=dumpnames
    file_combobox['state']='readonly'
    file_combobox.bind('<<ComboboxSelected>>',funprov)
    file_combobox.pack(fill=X, padx=10, pady=10)

    button=Button(win, text='CHIUDI', command=closewin)
    button.pack()

    win.mainloop()   

def plotlogbook(path):
    filename=path[len(PATHLOGBFOLDER)+1:-5]
    stats=pickle.load(open(path,"rb"))
    listavgrisk=[]
    listavgyield=[]
    for logb in stats:
        for stat in logb:
            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)
    graficoriskyield(listavgrisk,listavgyield,filename)

def graficoriskyield(listavgrisk,listavgyield,filename="File"):
    
    plt.style.use("ggplot")
    # fig, ((ax1,ax2,ax3,ax4)) = plt.subplots(nrows=4, ncols=1, sharex=True,figsize=(10, 8))
    fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(9, 6))

    maxtime=int(filename[filename.find("MAXTIME=")+8:filename.find("_TOURNPARAM")])
    date = pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listavgrisk))
    
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.8f}'))
  
    fig.suptitle(f"{filename}")
    
    ax1.plot(date,listavgyield,label=f"Y avg: {np.mean(listavgyield)}",color="green")
    ax1.set_title(f"Yield")
    ax1.set_ylabel("Yield")
    ax1.legend()

    ax2.plot(date,listavgrisk,label=f"R avg: {np.mean(listavgrisk)}",color="green")
    ax2.set_title(f"Risk")
    ax2.set_ylabel("% Rischio")
    ax2.set_xlabel(f'Data\n Dal {stockdf[0]["Date"][0]} al {stockdf[0]["Date"][maxtime-1]} maxtime:{maxtime}')
    ax2.legend()
    
    # fig.legend()
    plt.gcf().autofmt_xdate()
    plt.show()

stockdf,stocknames= genstockdf()
tkloadlogbook(gendumpnames())
# for df in stockdf:
#     print(df.index[-1])
