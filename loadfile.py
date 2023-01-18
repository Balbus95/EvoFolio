import pickle
import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re
from tkinter import *
from tkinter import ttk


ABSPATH=os.path.dirname(os.path.abspath(__file__))

def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

if(isWindows()): 
    PATHLOGBFOLDER= ABSPATH+"\\output\\logbook\\" #path per windows
else: PATHLOGBFOLDER= ABSPATH+"/output/logbook" #path per unix

if(isWindows()): 
    PATHGUADFOLDER= ABSPATH+"\\output\\guadagni\\" #path per windows
else: PATHGUADFOLDER= ABSPATH+"/output/guadagni" #path per unix

  
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

def gendumpnames(path):
        

    def lensort(filename):
        return len(filename[:filename.find("_MU")])

    dumpnames=[]
    pattern="*.dump"
    i=0
    for dump in os.listdir(path):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])
            i+=1
    dumpnames.sort(key=lensort)
    return dumpnames

def genportfolio(ind):
    listportfoliotitle=[]
    for i,stock in enumerate(stocknames):
        if(ind[i]!=0):
            listportfoliotitle.append(f'{stock}:{int(ind[i])}')
            # listportfoliotitle.append([stock,int(ind[i])])
    return listportfoliotitle

def tkloadfile(logbnames,guadagninames):
  
    win = Tk()
    win.title("PlotLoader")
    # win.geometry("300x150")

    def closewin():
        win.destroy()

    def plotall():
        loadall(os.path.join(PATHLOGBFOLDER, logb.get())+'.dump',os.path.join(PATHGUADFOLDER, guad.get())+'.dump')
    
    win.columnconfigure(0,weight=1)
    win.columnconfigure(1,weight=1)

    Label(win, text="Seleziona file da visualizzare").grid(column=0,row=0,columnspan=2,pady=2)
    
    logb=StringVar()
    logb_combobox = ttk.Combobox(win, textvariable=logb,justify=CENTER,width=75)
    logb_combobox.set("Lista Logbook")
    logb_combobox['values']=logbnames
    logb_combobox['state']='readonly'
    logb_combobox.grid(column=0,row=1,columnspan=2,pady=2,padx=5)
    # logb_combobox.bind('<<ComboboxSelected>>',selectlogb)
  
    guad=StringVar()
    guad_combobox = ttk.Combobox(win, textvariable=guad,justify=CENTER,width=75)
    guad_combobox.set("Lista Guadagni")
    guad_combobox['values']=guadagninames
    guad_combobox['state']='readonly'
    guad_combobox.grid(column=0,row=3,columnspan=2,pady=15,padx=5)
    # guad_combobox.bind('<<ComboboxSelected>>',selectguad)

    plotbutton=Button(win, text='PLOT', command=plotall,bg='#3A75C4',fg='white')
    plotbutton.grid(column=0, row=4,pady=10,padx=10,sticky='nesw')
    closebutton=Button(win, text='ESCI', command=closewin,bg='#7B1B02',fg='white')
    closebutton.grid(column=1, row=4,pady=10,padx=10,sticky='nesw')

    win.mainloop()   

def loadall(logbpath,guadpath):
    logbfile=logbpath[len(PATHLOGBFOLDER)+1:-5]
    guadfile=guadpath[len(PATHGUADFOLDER)+1:-5]
    logbooks=pickle.load(open(logbpath,"rb"))
    guadagni=pickle.load(open(guadpath,"rb"))
    
    listguadagni=[]
    maxguadagno=0
    for ind in guadagni:
        if ind[1]>=maxguadagno:
            maxguadagno=ind[1]
            bestind=[ind[0],genportfolio(ind[2])]
        listguadagni.append(ind[1])

    listavgrisk=[]
    listavgyield=[]
    for logb in logbooks:
        for stat in logb:
            avgrisk=stat["avg"][0]
            avgyield=stat["avg"][1]
            listavgrisk.append(avgrisk)
            listavgyield.append(avgyield)

    plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile)

def plotall(listguadagni,bestind,listavgrisk,listavgyield,logbfile,guadfile):

    regex="^[A-Z][a-z]+[_]?[ ]?[0-9]+|[A-Z\[a-z\]]+[=][0-9\[.\]]+"

    if re.findall(regex, logbfile)[1:]==re.findall(regex, guadfile)[1:]:
        matchguad= re.findall(regex, guadfile)
        
        plt.style.use("ggplot")
        fig = plt.figure(f"GRAFICO {str(matchguad[1:])[1:-1]}",figsize=(13,6))

        maxtime=int(str(matchguad[4])[8:])
        datelogb=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listavgrisk))
        dateguad=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][maxtime-1], periods=len(listguadagni))
        bestdate=pd.to_datetime(stockdf[0]["Date"][bestind[0]-1])
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    
        fig.suptitle(f"Miglior Portfolio il {str(bestdate)[:-9]}\n{bestind[1]}")
        
        yplt = plt.subplot2grid((3, 3), loc=(0, 0),colspan=3)
        yplt.plot(datelogb,listavgyield,label=f"Yield avg: {np.mean(listavgyield)}",color="green")
        yplt.set_title(f"Configurazione: {matchguad[1:]}")
        yplt.legend(frameon=False)

        rplt = plt.subplot2grid((3, 3), loc=(1, 0),colspan=3)
        rplt.plot(datelogb,listavgrisk,label=f"Risk avg: {np.mean(listavgrisk)}",color="red")
        rplt.legend(frameon=False)

        gplt = plt.subplot2grid((3, 3), loc=(2, 0),colspan=3)
        gplt.plot(dateguad,listguadagni,label=f"Valore Portfolio",color="blue",marker='o')
        gplt.scatter(bestdate,(np.max(listguadagni)),s=125,label=f"Guadagno Miglior Portfolio: {np.max(listguadagni)}")
        gplt.set_xlabel(f'Data\nDal {stockdf[0]["Date"][0]} al {stockdf[0]["Date"][maxtime-1]}') 
        gplt.legend(frameon=False)
        
        # fig.legend(loc="lower left", title="", frameon=False)
        fig.tight_layout(h_pad=-1)
        plt.gcf().autofmt_xdate()
        plt.show()
    else:
        return print("i file non hanno gli stessi parametri")

def main():
    tkloadfile(gendumpnames(PATHLOGBFOLDER),gendumpnames(PATHGUADFOLDER))

if __name__ == "__main__":
    stockdf,stocknames= genstockdf()
    main()
                            




