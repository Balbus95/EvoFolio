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

logbpathfolder=PATHGUADMONFOLDER


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

def genportfolio(ind): #returns the portfolio of ind with titles
    listportfoliotitle=[]
    for i,stock in enumerate(stocknames):
        if(ind[i]!=0):
            listportfoliotitle.append(f'{stock}:{int(ind[i])}')
            # listportfoliotitle.append([stock,int(ind[i])])
    return listportfoliotitle

def tkloadguadagni(dumpnames):
  
    win = Tk()
    win.title("Logbook Disponibili")
    win.geometry("600x80")

    def closewin():
        win.destroy()

    def funprov(event):
        path=os.path.join(logbpathfolder, file.get()+'.dump')
        plotguadagni(path)

    file=StringVar()
    file_combobox = ttk.Combobox(win, textvariable=file)
    file_combobox['values']=dumpnames
    file_combobox['state']='readonly'
    file_combobox.bind('<<ComboboxSelected>>',funprov)
    file_combobox.pack(fill=X, padx=10, pady=10)

    button=Button(win, text='CHIUDI', command=closewin)
    button.pack()

    win.mainloop()   

def plotguadagni(path):
    filename=path[len(logbpathfolder):-5]
    guadagni=pickle.load(open(path,"rb"))

    listportfolio=[]
    listguadagni=[]
    maxguadagno=0
    for ind in guadagni:
        if ind[1]>=maxguadagno:
            maxguadagno=ind[1]
            bestind=[ind[0],genportfolio(ind[2])]
        listguadagni.append(ind[1])
        listportfolio.append(genportfolio(ind[2]))

    graficoguadagni(listguadagni,bestind,filename)

def graficoguadagni(listguadagni,bestind,filename):
    
    paramRegex=r"^[A-Z\[a-z\]]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"
    matchguad= re.findall(paramRegex, filename)

    fig = plt.figure(f"PLOT OF {str(matchguad[1:])[1:-1]}",figsize=(12,6))

    maxtime=int(str(matchguad[4])[8:])

    plt.style.use("ggplot")

    dateguad=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listguadagni))
    
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.8f}'))
  
    fig.suptitle(f"Config: {str(filename)[7:]}")

    plt.plot(dateguad,listguadagni,label=f"Portfolio value",color="blue",marker='o')
    # gplt.plot(dateguad,listguadagni,label=f"Portfolio value with € {str(idfileRegex.search(matchguad[-1]).group())}",color="blue",marker='o')
    # gplt.plot(dateguad,listguadagni,label=f"Valore Portfolio con {str(matchguad[-1:])[2:-2]}€",color="blue",marker='o')
    # gplt.scatter(bestdate,(np.max(listguadagni)),s=125,label=f"Best Earnings Portfolio: {np.max(listguadagni)}")
    plt.ylabel("US Dollars $")
    plt.xlabel(f'Date\nfrom {stockdf[0]["Date"][0]} to {stockdf[0]["Date"][maxtime-1]}') 
    plt.legend(frameon=False)

    # fig.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig(f"loadfile_out/{filename}.pdf")
    plt.show()

stockdf,stocknames= genstockdf()
tkloadguadagni(gendumpnames())
# for df in stockdf:
#     print(df.index[-1])
