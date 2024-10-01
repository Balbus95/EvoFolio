import os,fnmatch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def isWindows():
    return os.name=="nt"

ABSPATH=os.path.dirname(os.path.abspath(__file__))
if(isWindows()): 
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" #path per windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" #path per unix
  
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

def saveStockToPDF():
    stockdf,stocknames= genstockdf()
    listclose=[]
    for df in stockdf:
        close=df["Close"].values.tolist()
        listclose.append(close)
    for i in range(len(listclose)):
        plt.style.use("ggplot")
        fig, ax = plt.subplots()
        datelogb=pd.date_range(stockdf[0]["Date"][0],stockdf[0]["Date"][len(listclose[i])-1], periods=len(listclose[i]))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
        ax.set_title(f"{stocknames[i]}")
        ax.set_ylabel(f"Close Price (USD)")
        ax.plot(datelogb,listclose[i],color="#069AF3")
        plt.gcf().autofmt_xdate()
        plt.savefig(f"stockToPDF_out/Close {stocknames[i]}.pdf")

saveStockToPDF()