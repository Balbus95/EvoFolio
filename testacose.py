import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

ABSPATH=os.path.dirname(os.path.abspath(__file__))

def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix

if(isWindows()): 
    PATHSTATSFOLDER= ABSPATH+"\\output\\logbook\\" #path per windows
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

stockdf,stocknames= genstockdf()
MAXTIME=24

def graficoriskyield(minrisk,minyield,maxrisk,maxyield,avgrisk,avgyield,stdrisk,stdyield):
    plt.style.use("ggplot")
    
    fig, ((ax1,ax2,ax3,ax4)) = plt.subplots(nrows=4, ncols=1, sharex=True,figsize=(10, 8))
    # fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(10, 7))
    date = pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][MAXTIME-1], periods=len(maxrisk))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    
    
    ax1.plot(date,minrisk,label="minrisk",color="blue")
    ax1.plot(date,maxrisk,label="maxrisk",color="red")
    ax1.set_ylabel("% Rischio")
    ax1.set_title(f"Popolazione")
    ax1.legend()

    ax2.plot(date,minyield,label="minyield",color="green")
    ax2.plot(date,maxyield,label="maxyield",color="blue")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("Rendimento")
    ax2.legend()

    ax3.plot(date,avgrisk,label="avgrisk",color="blue")
    ax3.plot(date,avgyield,label="avgyield",color="green")
    ax3.set_xlabel("Data")
    ax3.set_ylabel("AVG")
    ax3.legend()

    ax4.plot(date,stdrisk,label="stdrisk",color="blue")
    ax4.plot(date,stdyield,label="stdyield",color="green")
    ax4.set_xlabel("Data")
    ax4.set_ylabel("STD")
    ax4.legend()

    plt.gcf().autofmt_xdate()
    plt.show()   

stats=pickle.load(open(f"{PATHSTATSFOLDER}old\\MU=100_TOURNPARAM=0.7_SELPARAM=0.6_CXPB=0.9_NGEN=25__NDIM=47_stats.plk","rb"))
with open('logb.txt', 'w') as logb:
    for i in range(len(stats)):
        print(stats[i],file=logb)
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


if(len(listminrisk)==len(listminyield)==len(listmaxrisk)==len(listmaxyield)==len(listavgrisk)==len(listavgyield)==len(liststdrisk)==len(liststdyield)):
    print(f'lunghezza logbook: {len(listmaxyield)}')


# grafico(listriskmin,listriskmax)
# grafico(listyieldmin,listyieldmax)

graficoriskyield(listminrisk,listminyield,listmaxrisk,listmaxyield,listavgrisk,listavgyield,liststdrisk,liststdyield)

# pickle.dump(listyieldmax,open(f"output/MUs.plk","wb"))
# x=pickle.load(open("stock\\MUs.plk","rb"))
# print(x)
