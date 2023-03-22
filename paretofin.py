import random
import os,fnmatch
import itertools as iter
import pandas as pd
import numpy as np
import array
import pickle
from tkinter import *
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator, base, tools

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

def gendumpnames(path):  # returns a list of dump name 

    def lensort(filename):
        return len(filename[:filename.find("_MU")])

    dumpnames=[]
    pattern="*.dump"

    for dump in sorted(os.listdir(path)):
        if(dump!='.DS_Store' and fnmatch.fnmatch(dump, pattern)):
            dumpnames.append(dump[:-5])

    dumpnames.sort(key=lensort)
    return dumpnames

def genlisttuple(logbpathfolder,logbnames): # Returns a list of tuples with all risk and return avg of all files 
    listtuple=[]
    for dump in logbnames:
        logbpathfile=os.path.join(logbpathfolder, dump)+'.dump'
        logbooks=pickle.load(open(logbpathfile,"rb"))
        for logb in logbooks:
            for stat in logb:
                avgrisk=stat["avg"][0]
                avgyield=stat["avg"][1]
                listtuple.append([avgrisk,avgyield])

    return listtuple

def readind():
    global listtuple
    primoind=listtuple[0]
    listtuple.pop(0)
    return primoind

def myfitnessfake(ind):
    return (ind[0],ind[1])

def findbyfitness(pop,logbpathfolder,logbnames):
    listconfig=set()
    for ind in pop:
        for dump in logbnames:
            logbpathfile=os.path.join(logbpathfolder, dump)+'.dump'
            logbooks=pickle.load(open(logbpathfile,"rb"))
            for logb in logbooks:
                for stat in logb:
                    if (stat["avg"][0]==ind[0]) and (stat["avg"][1]==ind[1]):
                        listconfig.add(logbpathfile[logbpathfile.find("Logb"):])
    return listconfig

def minmaxind(pop):
    minr=min(ind[0] for ind in pop)
    maxy=max(ind[1] for ind in pop)
    for ind in pop:
        if(ind[0]==minr):
            minind=[ind[0],ind[1]]
        if(ind[1]==maxy):
            maxind=[ind[0],ind[1]]
    return minind,maxind
        
random.seed()
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)

logbpathfolder=PATHLOGBMONFOLDER
k=100
listtuple=genlisttuple(logbpathfolder,gendumpnames(logbpathfolder))

toolbox = base.Toolbox()
toolbox.register("attr_float", readind)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", myfitnessfake) 
toolbox.register("select", tools.selNSGA2)

pop = toolbox.population(n=len(listtuple)) # Population creation
pop = toolbox.select(pop, k)

listconfig=findbyfitness(pop,logbpathfolder,gendumpnames(logbpathfolder))
minind,maxind=minmaxind(pop)

print(f'\nBest risk and yield found among {str(logbpathfolder[logbpathfolder.find("output"):-9][7:])} dump:')
print(f'MIN RISK: {minind[0]} with yield {minind[1]}')
print(f'MAX YIELD: {maxind[1]} with risk {maxind[0]}')
print(f'The best configurations of the first {k} individuals of the pareto:')
for config in listconfig:
    print(config)