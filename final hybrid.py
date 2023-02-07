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

#### Default parameters 
MINAZIONI, MAXAZIONI= 10, 14 # min and max number of different stocks that a portfolio can hold
BUDG = 1000000 # initial budget of portfolios
BOUND_LOW, BOUND_UP = 0, BUDG # min and max number of equal stock that a portfolio can hold
MAXTIME=24 # maximum csv row to read, the row is the date in the csv, in this case using /stock/WEEK each csv row equals one week, 24 is 6 months, comment to use the maximum length of the csv
ELITEPARAM=0.3 # elite parameter, e.g. 0.3 selects 30% of the pop

#### These below are overwritten by the next "for", edit or remove them
MU = 100 # population size, number of individuals in the population.
TOURNPARAM= 0.9 # tournament parameter, e.g. 0.9 selects 90% of the pop
SELPARAM= 0.8 # NSGA-II selection parameter, e.g. 0.8 selects 80% of the pop
CXPB = 0.9 # probability of mating each individual at each generation 
NGEN = 250 # number of generation of nsga2

ABSPATH=os.path.dirname(os.path.abspath(__file__)) # takes the path of this folder
if(os.name=="nt"): # check of OS
    PATHCSVFOLDER= ABSPATH+"\\stock\\WEEK" # path windows
else: PATHCSVFOLDER= ABSPATH+"/stock/WEEK" # path unix

def genstockdf(pathfolder): # returns a list of dataframe and the list of stock names
    stockdf=[]
    stocknames=[] 
    pattern="*.csv"
    i=0
    for stock in sorted(os.listdir(pathfolder)):
        if(stock!='.DS_Store'and fnmatch.fnmatch(stock, pattern)):
            stocknames.append(stock[:-4])
            path=os.path.join(pathfolder, stocknames[i]+'.csv')
            df=pd.read_csv(path,usecols=["Date","Open","High","Low","Close","Adj Close","Volume"])
            stockdf.append(df)
            i+=1
    return (stockdf,stocknames)

def printpop(pop): # function for printing a population
    print(f"{len(pop)} - ", end='')
    for i in range(len(pop)):
        print(f"{str(pop[i])[16:-1]}", end=',')

def maxazione(stockdf): # returns the value of the most expensive action of the entire stock of actions
    maxcost=0
    for i in range(len(stockdf)):
        for row in range(1,len(stockdf[i])+1):
            cost = stockdf[i]["Close"][row-1]
            if cost > maxcost:
                maxcost=cost
    return maxcost

def minazione(stockdf): # returns the value of the least expensive action of entire stock of actions
    mincost=stockdf[0]["Close"][0]
    for i in range(len(stockdf)):
        for row in range(1,len(stockdf[i])+1):
            cost = stockdf[i]["Close"][row-1]
            if cost < mincost:
                mincost=cost
    return mincost

def combinator(len): # returns the list of possible combination of the entire stock of actions like [(0,1),(0,2),...,(last-1,last)]
        comb=[]
        for i in range(len):
            comb.append(i)
        comb=list(iter.combinations(comb, 2))
        return comb

def lucky(stockdf,ind): # returns portfolio's value calculated with the min of every action's value
    lowtotal=0
    for i in range(len(ind)):
        if(ind[i]!=0):
            low = (stockdf[i]["Low"][tempo-1])*ind[i]
            lowtotal+=low
    return lowtotal

def murphy(stockdf,ind): # returns portfolio's value calculated with the max of every action's value
    hightotal=0
    for i in range(len(ind)):
        if(ind[i]!=0):
            high = (stockdf[i]["High"][tempo-1])*ind[i]
            hightotal+=high
    return hightotal

def middle(stockdf,ind): # returns portfolio's value calculated with the mean of every action's value
    avgtotal=0
    for i in range(len(ind)):
        if(ind[i]!=0):
            low = (stockdf[i]["Low"][tempo-1])*ind[i]
            high = (stockdf[i]["High"][tempo-1])*ind[i]
            avg=(low+high)/2
            avgtotal+=avg
    return avgtotal

def middlestart(stockdf,ind): # equals to middle() but is only used to generate the portfolios with genind()
    avgtotal=0
    for i in range(len(ind)):
        if(ind[i]!=0):
            low = (stockdf[i]["Low"][0])*ind[i]
            high = (stockdf[i]["High"][0])*ind[i]
            avg=(low+high)/2
            avgtotal+=avg
    return avgtotal

def conta_azioni_possedute(ind): # return the number of different actions purchased in the portfolio 
    count=0
    for num in ind:
        if(num==0):
            count+=1
    return len(ind)-count

def set_tkPREF(): # GUI used for choosing the list of favorite stocks
    
    win = Tk()
    win.title("Stock")
    # win.geometry("700x250")
    checkboxes = {}

    def genPREF():
        global PREF
        if (len(PREF)==0):
            for box in checkboxes:
                PREF.append(box.var.get())
            # print('PREFERITI SETTATI',PREF)
            win.destroy()
        elif (len(PREF)==len(checkboxes)):
            PREF=[]
            for box in checkboxes:
                PREF.append(box.var.get())
            # print('PREFERITI SETTATI',PREF)
            win.destroy()
        else: print("IMPOSSIBILE")


    def ShowCheckBoxes(stocknames):
        Cbcolumn = 1
        Cbrow = 5
        Chkcount = 0

        for Checkbox in range(len(stocknames)):
            name = stocknames[Checkbox]
            indpref = Checkbox
            current_var = IntVar()
            current_box = Checkbutton(win, text=name, variable=current_var)
            current_box.var = current_var
            current_box.grid(row=Cbrow, column=Cbcolumn)
            checkboxes[current_box] = indpref 
            if Cbcolumn == 6:
                Cbcolumn = 1
                Cbrow += 1
            else:
                Cbcolumn += 1
            Chkcount += 1
        Button(win, text='CONFIRM', command=genPREF,bg='#3A75C4',fg='black').grid(row=Cbrow+1, column=2, columnspan=4,pady=5)

    Label(win, text="Select favorite stocks",pady=5).grid(row=0, column=2, columnspan=4)
    ShowCheckBoxes(stocknames)
    win.mainloop()

def getTitlePREF(listpref): # returns the list of favorite stock names
    listpreftitle=[]
    if listpref:
        for i,stock in enumerate(stocknames):
            if(listpref[i]==1):
                listpreftitle.append(stock)
    else: return listpreftitle
    return listpreftitle

def genelite(pop,pref): # returns a list of individuals who have multiple preferred actions
    indliked=[]
    for i in range(len(pref)):
        if(pref[i]==1):
            indmaxazioni=0
            for ind in pop:
                if(ind[i]>=indmaxazioni):
                    indmaxazioni=ind[i]
                    maxind=ind
            indliked.append(maxind)
    return indliked

def closestMultiple(n,mult=4): #find the closest minor multiple
    x=n%mult
    z=n-x 
    return z

def calclistyield(df,col,tempo): # Yield calculation function
    """
    param df: dataframe of a stock
    param col: column to calculate
    param tempo: df row until which time to calculate
    """
    listyield=[]
    if tempo>=2:
        for i in reversed(range(1,len(df[col][:tempo]))):
            listyield.append(np.log(df[col][tempo-i]/df[col][tempo-i-1]))
        return listyield
    else: 
        listyield=[0]
        return listyield

def calccov(list1,list2,tempo): # Covariance calculation function
    """
    param list1: list of yields of the first stock
    param list2: list of yields of the second stock
    param tempo: df row until which time to calculate
    """
    if tempo>=3:
        cov=np.cov(list1,list2)
        cov=float(cov[1][0])
        return cov
    else:
        return 0 

def calcrisk(az1,az2,var1,var2,cov): # Risk calculation function
    """
    param az1: percentage of the number of shares of the first stock respect to portfolio
    param az2: percentage of the number of shares of the second stock respect to portfolio
    param var1: variance of the first stock
    param var2: variance of the first stock
    param cov: covariance of the first and second stock
    """
    risk=(az1*var1)+(az2*var2)+(2*(az1*az2*cov)) 
    return risk

def myfitness(ind): # function that returns an individual's fitness, returns total risk and total yield
    comb=combinator(len(ind))
    listyield=[]
    listvar=[]
    listrisk=[]
    totyield=0
    for i in range(len(ind)):
        if(ind[i]!=0):
            df=stockdf[i]
            yeld=calclistyield(df,"Close",tempo)
            listyield.append(yeld)
            listvar.append(np.var(yeld))
            totyield += ind[i]*np.mean(yeld)
        else:
            listyield.append(0)
            listvar.append(0)
    for coppia in comb:
        if(ind[coppia[0]]!=0 and ind[coppia[1]]!=0):
            x=coppia[0]
            y=coppia[1]
            risk=calcrisk(ind[x]/sum(ind),ind[y]/sum(ind),listvar[x],listvar[y],calccov(listyield[x],listyield[y],tempo))
            listrisk.append(risk)
    totrisk=sum(listrisk)
    return (totrisk,totyield)

def genind_old(low,up,size): # function for generating random portfolio,  utilizzato per esperimento 1,2 con nuove mate e mutate di examples/ga/nsga2.py
    """ Customized generator of individual. Checks for its validity based on budget's constraints.
        param low: min number of equal stock that a portfolio can hold.
        param up: max number of equal stock that a portfolio can hold.
        param size: portfolio size (number of stock's files). """
    maxbudg=BUDG+1
    while maxbudg>BUDG:
        ind=[0 for i in range(size)] # initialization of portfolio
        numstock=random.randint(MINAZIONI,MAXAZIONI) # random number of different stocks to buy for this portfolio 
        stockused=[]  # list of actions already used (bought)
        for i in range(numstock): 
            stock=random.randint(0,size-1) # randomly chooses the 'stock' to buy for this portfolio
            while stock in stockused: 
                stock=random.randint(0,size-1) # stock has already been used, so try again with another random stock
            stockused.append(stock) # 'stock' has been used, so it adds stock to the list of used stock
            ind[stock]=random.randint(low+1,up) # random number of actions to buy of 'stock'
        maxbudg=middlestart(stockdf,ind) # check whether the portfolio value is too high
    return ind # returns the generated portfolio 

def genind(low,up,size): # function for generating random portfolio, utilizzato per esperimento 3 con nuove mate e mutate mutUniformIntAdaptive
    """ Customized generator of individual. Checks for its validity based on budget's constraints.
        param low: min number of equal stock that a portfolio can hold.
        param up: unused for this version.
        param size: portfolio size (number of stock's files). """
    maxbudg=BUDG+1
    while maxbudg>BUDG:
        ind=[0 for i in range(size)]  # initialization of portfolio
        numstock=random.randint(MINAZIONI,MAXAZIONI) # random number of different stocks to buy for this portfolio
        stockused=[] # list of actions already used (bought)
        currentbudg=BUDG #money in bank account
        for i in range(numstock):
            stock=random.randint(0,size-1) # randomly chooses the 'stock' to buy for this portfolio
            while stock in stockused:
                stock=random.randint(0,size-1) # stock has already been used, so try again with another random stock
            stockused.append(stock)  # 'stock' has been used, so it adds stock to the list of used stock
            upperbound_default=int(currentbudg/np.max(stockdf[stock]["Close"])) #max no. of stocks of type 'stock' purchasable with my current money
            if upperbound_default>1:
                ind[stock]=random.randint(low+1,upperbound_default) # random number of actions to buy of 'stock'
            currentbudg=BUDG-middlestart(stockdf,ind) #update current money available
        maxbudg=int(middlestart(stockdf,ind))  # check whether the portfolio value is too high
    return ind # returns the generated portfolio 

stockdf,stocknames = genstockdf(PATHCSVFOLDER) 
NDIM = len(stockdf) #portfolio size (number of stock's files)
countfile=1

# Setting favourite stocks
PREF=[] 
set_tkPREF()
preftitle=getTitlePREF(PREF)

# Registration object of deap and functions to generate population individuals
random.seed()
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)
toolbox = base.Toolbox()
toolbox.register("attr_float", genind, BOUND_LOW, BOUND_UP, NDIM) #generation portfolios
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float) #crates an individuals with attr_float
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #repeates the "individual" function

#### Adapt maxtime to csv with fewer rows
# MAXTIME=len(stockdf[0])
# for df in stockdf:
#     if len(df)<MAXTIME:
#         MAXTIME=len(df)

print(f"\nSTOCK NAMES {len(stocknames)} :\n{stocknames}\n")
print(f'FAVORITE STOCK {len(preftitle)} : {preftitle}\n')
while True: # Choose of configuration
    choose=input("Select a configuration\nType 1 for monthly and 2 for trimestral: ")
    if choose == '1':
        foldertosave="mensile"
        offset=4
        print("You chose monthly\n")
        break
    elif choose == '2':
        foldertosave="trimestrale"
        offset=12
        print("You chose trimestral\n")
        break
    else:
        print("Invalid Case, retry\n")

for TOURNPARAM in [0.9,0.7,0.5]: #for different configuration of TOURNPARAM , this overrides default parameter
    print(f'TOURNPARAM:{TOURNPARAM}', end=', ')
    for SELPARAM in [0.8,0.6,0.4]:  #for different configuration of SELPARAM, this overrides default parameter
        print(f'SELPARAM:{SELPARAM}', end=', ')
        for CXPB in [0.9,0.7,0.5]:  #for different configuration of CXPB, this overrides default parameter
            print(f'CXPB:{CXPB}', end=', ')
            for MU in [250,500,1000]: #for different configuration of MU, this overrides default parameter
                pop = toolbox.population(n=MU) #population creation
                print(f'MU:{MU}', end=', ')
                for NGEN in [10,50,100,200]:  #for different configuration of NGEN, this overrides default parameter
                    print(f'NGEN:{NGEN}')
                    statslist=[]
                    listguadagno=[]
                    relativebudget=BUDG
                    print(f"{countfile}) MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG} - STARTED")
                    if (not (os.path.isfile(f"output/{foldertosave}/guadagni/Guad_{countfile}_MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG}.dump") and os.path.isfile(f"output/{foldertosave}/logbook/Logb_{countfile}_MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG}.dump"))):
                        for tempo in range(offset,MAXTIME+1,offset): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY
                            
                            # Registration functions for genetic and fitness operators
                            toolbox.register("evaluate", myfitness) #registration of fitness function
                            toolbox.register("mate", tools.cxOnePoint)
                            toolbox.register("mutate", tools.mutUniformIntAdaptive, low=BOUND_LOW, up=relativebudget, indpb=1.0/NDIM,dfstocks=stockdf) #custom function, use 'relativebudget' and stockdf
                            # toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0) #crossover function customized for return a INT
                            # toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM) #mutation function customized for return a INT
                            toolbox.register("select", tools.selNSGA2) # selection function

                            def main():
                                global pop
                                data=str(pd.to_datetime(stockdf[0]["Date"][tempo-1]))[:-9] # -9 taglia i caratteri dei hh:mm:ss dalla stringa
                                print(f"TIME {tempo} ---- {data}")
                                pop,logbook=nsga2(pop) #pop is iterated 'tempo' times, using the pop of the previous call for the new call of nsga2()
                                statslist.append(logbook)

                            def nsga2(pop): # nsga2 algorithm of deap modified, the line next to #C is a custom line.
                                
                                global relativebudget

                                stats = tools.Statistics(lambda ind: ind.fitness.values)
                                stats.register("avg", np.mean, axis=0)
                                stats.register("std", np.std, axis=0)
                                stats.register("min", np.min, axis=0)
                                stats.register("max", np.max, axis=0)

                                logbook = tools.Logbook()
                                logbook.header = "gen", "evals", "std", "min", "avg", "max"

                                if tempo>offset: #C
                                    relativebudget+=middle(stockdf,pop[0])
                                    listguadagno.append([tempo,relativebudget,[i for i in pop[0]]])

                                # Evaluate the individuals with an invalid fitness
                                invalid_ind = [ind for ind in pop if not ind.fitness.valid]
                                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                                for ind, fit in zip(invalid_ind, fitnesses):
                                    ind.fitness.values = fit

                                # Decreases one stock at a time until the portfolio is within budget #C
                                for ind in pop:
                                    cb=middle(stockdf,ind)
                                    while cb>relativebudget:
                                        r=random.randint(0,len(ind)-1)
                                        while ind[r]==0 or (ind[r]==1 and conta_azioni_possedute(ind)==MINAZIONI):
                                            r=random.randint(0,len(ind)-1)
                                        ind[r]-=1
                                        cb=middle(stockdf,ind)
                                
                                # Checks the integrity of the portfolio #C
                                pop = [ind for ind in pop if (conta_azioni_possedute(ind)>=MINAZIONI and conta_azioni_possedute(ind)<=MAXAZIONI)]
                                
                                # This is just to assign the crowding distance to the individuals #C
                                pop = toolbox.select(pop, int(len(pop)*SELPARAM))

                                record = stats.compile(pop) #compile() Applica ai dati della sequenza di input ogni funzione registrata e restituisce un dizionario. 
                                logbook.record(gen=0, evals=len(invalid_ind), **record)
                                # print(logbook.stream) #print header e gen0
 
                                # Begin the generational process
                                for gen in range(1, NGEN):
                                    
                                    #C creates an elite population
                                    elite=genelite(pop,PREF)
                                    elite = [toolbox.clone(ind) for ind in elite]

                                    # Vary the population #C
                                    offspring = tools.selTournamentDCD(pop, closestMultiple(int(len(pop)*TOURNPARAM)))
                                    offspring = [toolbox.clone(ind) for ind in offspring]

                                    # mutate and crossover
                                    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):

                                        if random.random() <= CXPB:
                                            toolbox.mate(ind1, ind2)
                                        
                                        toolbox.mutate(ind1)
                                        toolbox.mutate(ind2)
                                        del ind1.fitness.values, ind2.fitness.values

                                    # mutate and crossover with elite #C
                                    for ind1 in elite:
                                        for ind2 in offspring:

                                            if random.random() <= ELITEPARAM:
                                                toolbox.mate(ind1, ind2)
                        
                                            toolbox.mutate(ind1)
                                            toolbox.mutate(ind2)
                                            del ind1.fitness.values, ind2.fitness.values

                                    # Decreases one stock at a time until the portfolio is within budget #C
                                    for ind in offspring: 
                                        cb=middle(stockdf,ind)
                                        while cb>relativebudget:
                                            r=random.randint(0,len(ind)-1)
                                            while ind[r]==0 or (ind[r]==1 and conta_azioni_possedute(ind)==MINAZIONI):
                                                r=random.randint(0,len(ind)-1)
                                            ind[r]-=1
                                            cb=middle(stockdf,ind)

                                    # Checks the integrity of the portfolio #C
                                    offspring = [ind for ind in offspring if (conta_azioni_possedute(ind)>=MINAZIONI and conta_azioni_possedute(ind)<=MAXAZIONI)] #cancella individui che hanno maxzeri azioni a 0

                                    # Evaluate the individuals with an invalid fitness
                                    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                                    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                                    for ind, fit in zip(invalid_ind, fitnesses):
                                        ind.fitness.values = fit

                                    # Select the next generation population
                                    pop = toolbox.select(pop + offspring, MU)
                            
                                    record = stats.compile(pop)
                                    logbook.record(gen=gen, evals=len(invalid_ind), **record)
                                    # print(logbook.stream) #print row gen

                                # print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))
                                relativebudget-=middle(stockdf,pop[0]) # earnings calculation 

                                if tempo==offset: #C
                                    listguadagno.append([tempo,relativebudget+middle(stockdf,pop[0]),[i for i in pop[0]]])
                                elif tempo==MAXTIME:
                                    relativebudget+=middle(stockdf,pop[0])
                                    listguadagno.append([tempo,relativebudget,[i for i in pop[0]]])

                                return pop ,logbook

                            if __name__ == "__main__":
                                main()

                        # save .dump files
                        pickle.dump(listguadagno,open(f"output/{foldertosave}/guadagni/Guad_{countfile}_MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG}.dump","wb"))
                        pickle.dump(statslist,open(f"output/{foldertosave}/logbook/Logb_{countfile}_MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG}.dump","wb"))
                        print(f"{countfile}) MU={MU} NDIM={NDIM} NGEN={NGEN} MAXTIME={MAXTIME} TOURNPARAM={TOURNPARAM} SELPARAM={SELPARAM} CXPB={CXPB} BUDG={BUDG} - END\n")
                        countfile+=1

                    else: 
                        countfile+=1
                        print('Configuration already done\n')
