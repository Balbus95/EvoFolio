import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from deap import creator, base, tools

ABSPATH=os.path.dirname(os.path.abspath(__file__))

def isWindows():
    return os.name=="nt"

if(isWindows()): 
    PATHSTATSFOLDER= ABSPATH+"\\output\\stats\\" #path per windows
else: PATHSTATSFOLDER= ABSPATH+"/output/stats/" #path per unix

if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix
  


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
MAXTIME=12

def grafico(min,max):
    plt.style.use("ggplot")
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=4, ncols=1, sharex=True)
    # date=pd.to_datetime(stockdf[0]["Date"]) 
    date=pd.to_datetime(stockdf[0]["Date"][:MAXTIME]) 
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
    # plt.plot(date,valorimax,label="max",color="red")
    ax1.plot(date,min,label="min",color="blue")
    ax2.plot(date,max,label="max",color="red")
    ax3.plot(date,max,label="max",color="green")
    ax4.plot(date,max,label="max",color="black")
    # plt.plot(date,list,label="max1",color="red")
    # plt.plot(date,list,label="max1",color="red")
    # plt.plot(date,list,label="max1",color="red")
    # plt.plot(date,valorimin,label="min",color="green")
    ax1.set_title(f"Portfolio")
    ax1.set_xlabel("Data")
    ax1.set_xlabel("Data")
    # ax1.set_xticks(rotation=20)
    ax1.set_ylabel("Valore")
    ax1.set_ylabel("Valore")
    fig.legend()
    # plt.grid()
    # plt.gcf().autofmt_xdate()
    plt.show()   

# stats=pickle.load(open("MU=1_TOURNPARAM=0.9_SELPARAM=0.8_CXPB=0.9_NGEN=10_guadagni","rb"))
# print(type(stats[0]))

stats=pickle.load(open(f"{PATHSTATSFOLDER}MU=48_TOURNPARAM=0.5_SELPARAM=0.4_CXPB=0.5_NGEN=50__NDIM=47_stats.plk","rb"))
print(stats[0])
#print(stats)
listriskmin=[]
listriskmax=[]
listyieldmin=[]
listyieldmax=[]

for i,stat in enumerate(stats):
    gen, max, min = stat.select("gen", "max", "min")
    print(i)
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

print(f'listriskmin: {listriskmin}')
print(f'listriskmax: {listriskmax}')
print(f'listyieldmin: {listyieldmin}')
print(f'listyieldmax: {listyieldmax}')


#grafico(listriskmin,listriskmax)
#grafico(listyieldmin,listyieldmax)

grafico(listriskmax,listyieldmin)

# pickle.dump(listyieldmax,open(f"output\\MUs.plk","wb"))
# pickle.load(open("stock/MUs.plk","rb"))
