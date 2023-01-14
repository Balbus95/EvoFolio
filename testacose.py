import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

def grafico(min,max):
    plt.style.use("ggplot")
    fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    # fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True)
    date=pd.to_datetime(stockdf[0]["Date"][:MAXTIME]) 
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.plot(date,valorimax,label="max",color="red")
    ax1.plot(date,min,label="min",color="blue")
    ax1.set_ylabel("% Rischio")
    ax1.set_title(f"Portfolio")
    # ax3.plot(date,max,label="max",color="green")
    # ax4.plot(date,max,label="max",color="black")

    ax2.plot(date,max,label="max",color="red")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("Rendimento")
    # ax1.set_xticks(rotation=20)
    fig.legend()
    # plt.grid()
    # plt.gcf().autofmt_xdate()
    plt.show()   

stats=pickle.load(open(f"{PATHSTATSFOLDER}Logbook_1_MU=48_TOURNPARAM=0.9_SELPARAM=0.8_CXPB=0.9_NGEN=10_NDIM=47_MAXTIME=24","rb"))
listriskmin=[]
listriskmax=[]
listyieldmin=[]
listyieldmax=[]
i=0
for stat in stats:
    gen, max, min = stat.select("gen", "max", "min")
    print(stat)
    print(f'minrisk: {min[i][0]}')
    print(f'maxrisk: {max[i][0]}')
    print(f'minyield: {min[i][1]}')
    print(f'maxyield: {max[i][1]}')
    minrisk=min[i][0]
    maxrisk=max[i][0]
    minyield=min[i][1]
    maxyield=max[i][1]
    listriskmin.append(minrisk)
    listriskmax.append(maxrisk)
    listyieldmin.append(minyield)
    listyieldmax.append(maxyield)
    #print(str(gen),' sdsd',str(max))

# print(f'listriskmin: {listriskmin}')
# print(f'listriskmax: {listriskmax}')
# print(f'listyieldmin: {listyieldmin}')
# print(f'listyieldmax: {listyieldmax}')


# grafico(listriskmin,listriskmax)
# grafico(listyieldmin,listyieldmax)

grafico(listriskmax,listyieldmin)

# pickle.dump(listyieldmax,open(f"output/MUs.plk","wb"))
# x=pickle.load(open("stock\\MUs.plk","rb"))
# print(x)
