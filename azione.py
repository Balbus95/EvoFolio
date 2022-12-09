import random
import pandas as pd
import numpy as np
from deap import creator, base, tools, algorithms


PortfolioNames=["Apple","Amazon","Tesla"]
PortfolioValue=[1,2,17]
portfolio=[["Apple",1],["Amazon",2],["Tesla",17]]

def tofloat(str):
    str=str.replace(",", "." )
    str=str.strip(" $")
    str=float(str)
    return str

def calcyield(ultimo,penultimo,azioni):
    yeld = azioni * np.log(ultimo/penultimo)
    return yeld

def maxyield():
    return random.randint(0,100)

def minrisk():
    return random.randint(0,100)

def generacosto():
    return random.randint(0,1000)

def topercento(perc):
    percf= f"{perc}%"
    return percf

def toeuro(euro):
    eurof= f"{euro}€"
    return eurof

def gentitle(numazioni):
    title=f"{numazioni} AZIONI"
    return title

def generaportfolio(name,value):
    title=gentitle(len(name))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    if len(name)==len(value):
        for i in range(len(name)):
            cost= toeuro(generacosto())
            yeld= topercento(maxyield())
            risk= topercento(minrisk())
            print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name[i],value[i],cost,yeld,risk))

def genport2(lista):
    title=gentitle(len(lista))
    print(f'{title:-^69}')
    print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format('Nome','Possedute','Costo','Guadagno','Rischio'))
    for y in lista:
        name,value=y
        cost= toeuro(generacosto())
        yeld= topercento(maxyield())
        risk= topercento(minrisk())
        print("{:<12}| {:<12}| {:<12}| {:<12}| {:<12}|".format(name,value,cost,yeld,risk))

#generaportfolio(PortfolioNames,PortfolioValue)
#print("\n")
#genport2(portfolio)

#df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=["Open", "High", "Low"])
#df = pd.read_csv(r'/Users/balbus/Documents/GitHub/evoport/stock/WEEK/ADBE.csv',sep = ',',usecols=[1,2,3,4,5])
df = pd.read_csv('ADBE.csv',usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
df["Low"][1]+df["Low"][0]

df1=pd.read_csv('example.csv',usecols=["Apple", "Amazon", "Telsa"], nrows=5)
i=4
azioni=PortfolioValue[0]
print(azioni)
ultimo = df1["Apple"][i]
penultimo = df1["Apple"][i-1]
ultimo= tofloat(ultimo)
penultimo= tofloat(penultimo)
print(type(ultimo))
print(ultimo+penultimo)
yeld = calcyield(ultimo,penultimo,azioni)
#x=(df1["Apple"][4])(df1["Apple"][3])
#yeld = 1 * np.log(df1["Close"][4]/df1["Close"][3])
#yeld = calcyield(df1,4,1)
#print(yeld)
print(df1)
print(yeld)







