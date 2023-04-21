import pickle
import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from tkinter import *
from tkinter import ttk
import re


ABSPATH=os.path.dirname(os.path.abspath(__file__))

if(os.name=="nt"): #path per windows
    PATHCSVFOLDER=ABSPATH+"\\stock\\WEEK\\" 
    PATHLOGBMONFOLDER=ABSPATH+"\\output\\mensile\\logbook\\"
    PATHGUADMONFOLDER=ABSPATH+"\\output\\mensile\\guadagni\\"
    PATHLOGBTRIFOLDER=ABSPATH+"\\output\\trimestrale\\logbook\\"
    PATHGUADTRIFOLDER=ABSPATH+"\\output\\trimestrale\\guadagni\\"
else: #path per unix
    PATHCSVFOLDER=ABSPATH+"/stock/WEEK/" 
    PATHLOGBMONFOLDER=ABSPATH+"/output/mensile/logbook/"
    PATHGUADMONFOLDER=ABSPATH+"/output/mensile/guadagni/"
    PATHLOGBTRIFOLDER=ABSPATH+"/output/trimestrale/logbook/"
    PATHGUADTRIFOLDER=ABSPATH+"/output/trimestrale/guadagni/"

logbpathfolder=PATHLOGBMONFOLDER


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
    for dump in os.listdir(logbpathfolder):
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
        path=os.path.join(logbpathfolder, file.get()+'.dump')
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
    filename=path[len(logbpathfolder):-5]
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

def plotlogbooktime(path):
    filename=path[len(logbpathfolder):-5]
    stats=pickle.load(open(path,"rb"))
    for i,logb in enumerate(stats):
        listavgrisk=[]
        listavgyield=[]
        for stat in logb:
            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)
        graficoriskyieldtime(listavgrisk,listavgyield,filename,i+1)

def graficoriskyield(listavgrisk,listavgyield,filename):
    
    paramRegex=r"^[A-Z\[a-z\]]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"
    matchlogb= re.findall(paramRegex, filename)

    fig = plt.figure(f"PLOT OF {str(matchlogb[1:])[1:-1]}",figsize=(12,6))

    maxtime=int(str(matchlogb[4])[8:])

    plt.style.use("ggplot")

    datelogb=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listavgrisk))
    
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.8f}'))
  
    fig.suptitle(f"Config: {str(filename)[7:]}")
    
    yplt = plt.subplot2grid((2, 2), loc=(0, 0),colspan=2)
    yplt.plot(datelogb,listavgyield,label=f"Yield avg: {np.mean(listavgyield)}",color="green")
    # yplt.set_title(f"Config: {str(matchlogb[1:-1])[1:-1]}")
    yplt.legend(frameon=False)

    rplt = plt.subplot2grid((2, 2), loc=(1, 0),colspan=2)
    rplt.plot(datelogb,listavgrisk,label=f"Risk avg:  {np.mean(listavgrisk)}",color="red")
    rplt.legend(frameon=False)
    rplt.set_xlabel(f'Date\nfrom {stockdf[0]["Date"][0]} to {stockdf[0]["Date"][maxtime-1]}') 
    # fig.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig(f"loadfile_out/{filename}.pdf")
    plt.show()

def graficoriskyieldtime(listavgrisk,listavgyield,filename,time=None):
    
    paramRegex=r"^[A-Z\[a-z\]]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"
    matchlogb= re.findall(paramRegex, filename)

    fig = plt.figure(f"PLOT OF {str(matchlogb[1:])[1:-1]}_time={time}",figsize=(12,6))

    plt.style.use("ggplot")

    ngenlistlabel=list(range(int(str(matchlogb[3])[str(matchlogb[3]).find("=")+1:])))

    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.8f}'))
  
    fig.suptitle(f"Config: {str(filename)[7:]}\nTime {time}")
    
    yplt = plt.subplot2grid((2, 2), loc=(0, 0),colspan=2)
    yplt.plot(ngenlistlabel,listavgyield,label=f"Yield avg: {np.mean(listavgyield)}",color="green")
    # yplt.set_title(f"Config: {str(matchlogb[1:-1])[1:-1]}")
    yplt.legend(frameon=False)

    rplt = plt.subplot2grid((2, 2), loc=(1, 0),colspan=2)
    rplt.plot(ngenlistlabel,listavgrisk,label=f"Risk avg:  {np.mean(listavgrisk)}",color="red")
    rplt.legend(frameon=False)
    rplt.set_xlabel(f'Number of generation = {matchlogb[3][str(matchlogb[3]).find("=")+1:]}') 
    # fig.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig(f"loadfile_out/{filename}_time={time}.pdf")
    plt.show()

stockdf,stocknames= genstockdf()
tkloadlogbook(gendumpnames())
# for df in stockdf:
#     print(df.index[-1])
