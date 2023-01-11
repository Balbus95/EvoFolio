with open('terminalout.txt', 'w') as term, open('log.txt', 'w') as logb:
    
    import random
    import time
    import os
    import itertools as iter
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import array
    import pickle
    from tkinter import *


    from deap.benchmarks.tools import diversity, convergence, hypervolume
    from deap import creator, base, tools

    def isWindows():
        return os.name=="nt"

    MAXAZIONI= 14
    MINAZIONI= 10


    ABSPATH=os.path.dirname(os.path.abspath(__file__))

    if(isWindows()): 
        PATHCSVFOLDER= ABSPATH+"\\stock\\full" #path per windows
    else: PATHCSVFOLDER= ABSPATH+"/stock/full" #path per unix
  
    # pass: msmtis_pwd

    def genstockdf():
        stockdf=[]
        stocknames=[] 
        i=0
        for stock in os.listdir(PATHCSVFOLDER):
            if(stock!='.DS_Store'):
                stocknames.append(stock[:-4])
                path=os.path.join(PATHCSVFOLDER, stocknames[i]+'.csv')
                df=pd.read_csv(path,usecols=["Date","Open", "High", "Low","Close","Adj Close","Volume"])
                stockdf.append(df)
                i+=1
        return (stockdf,stocknames)

    def maxazione(stockdf):
        maxcost=0
        for i in range(len(stockdf)):
            for row in range(1,len(stockdf[i])+1):
                cost = stockdf[i]["Close"][row-1]
                if cost > maxcost:
                    maxcost=cost
        return maxcost

    def printpop(pop):
        print(f"{len(pop)} - ", end='',file=term)
        for i in range(len(pop)):
            print(f"{str(pop[i])[16:-1]}", end=',',file=term)

    def combinator(len):
            comb=[]
            for i in range(len):
                comb.append(i)
            comb=list(iter.combinations(comb, 2))
            return comb

    def middle(stockdf,ind):
        avgtotal=0
        for i in range(len(stockdf)):
                low = (stockdf[i]["Low"][tempo-1])*ind[i]
                high = (stockdf[i]["High"][tempo-1])*ind[i]
                avg=(low+high)/2
                # print(f"avg {high} + {low} /2 = {avg}")
                avgtotal+=avg
        # print(f"avgtotal: {avgtotal}")
        return avgtotal

    def conta_azioni_possedute(ind):
        count=0
        for num in ind:
            if(num==0):
                count+=1
        return len(ind)-count

    def genind(low,up,size):
        ind=[0 for i in range(size)]
        numstock=random.randint(MINAZIONI,MAXAZIONI)
        stockused=[]
        for i in range(numstock):
            stock=random.randint(0,size-1)
            while stock in stockused:
                stock=random.randint(0,size-1)
            stockused.append(stock)
            ind[stock]=random.randint(low+1,up)
        return ind

    def set_tkPREF():
        
        root = Tk()
        root.title("Stock Azioni")
        # root.geometry("700x250")
        checkboxes = {}

        def genPREF():
            global PREF
            if (len(PREF)==0):
                for box in checkboxes:
                    PREF.append(box.var.get())
                print('button',PREF)
                root.destroy()
            elif (len(PREF)==len(checkboxes)):
                PREF=[]
                for box in checkboxes:
                    PREF.append(box.var.get())
                print('button',PREF)
                root.destroy()
            else: print("impossibile")


        def ShowCheckBoxes(stocknames):
            Cbcolumn = 0
            Cbrow = 4
            Chkcount = 0

            for Checkbox in range(len(stocknames)):
                name = stocknames[Checkbox]
                indpref = Checkbox
                current_var = IntVar()
                current_box = Checkbutton(root, text=name, variable=current_var)
                current_box.var = current_var
                current_box.grid(row=Cbrow, column=Cbcolumn)
                checkboxes[current_box] = indpref  # so checkbutton object is the key and value is string
                if Cbcolumn == 4:
                    Cbcolumn = 0
                    Cbrow += 1
                else:
                    Cbcolumn += 1
                Chkcount += 1

        Button(root, text='CONFERMA AZIONI PREFERITE', command=genPREF).grid(row=100, column=1, columnspan=3)
        ShowCheckBoxes(stocknames)# nessuna pref
        root.mainloop()

    def getTitlePREF(listpref):
        listpreftitle=[]
        for i,stock in enumerate(stocknames):
            if(listpref[i]==1):
                listpreftitle.append(stock)
        return listpreftitle

    def closestMultiple(n, x=4):
        if x>n:
            return x
        z=int(x / 2)
        n=n+z
        n=n-(n%x)
        return n

    def uniform(low, up, size=None): #non usata
        try:
            return [random.randint(a,b) for a, b in zip(low, up)] #viene ripetuto per MU volte
        except TypeError:  #non so perchè fa 4 giri nell'except, returna al try il numero per NDIM volte 
            return [random.randint(a,b) for a, b in zip([low] * size, [up] * size)]

    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)

    stockdf,stocknames = genstockdf()
    comb=combinator(len(stockdf))
    maxtime=len(stockdf[0])
    maxtime=11


    PREF=[]
    set_tkPREF()
    preftitle=getTitlePREF(PREF)
    # PREF=[0 for i in range(len(stockdf))] # nessuna pref

    BUDG = 100000
    BOUND_LOW, BOUND_UP = 0, int(BUDG/maxazione(stockdf)) # 0,10
    NDIM = len(stockdf) #dimensione singola tupla default 30 # lunghezza portafoglio (numero di azioni disponibili)

    MU = 100 #generazione tuple population, deve essere multiplo di 4 (Dimensione popolazione)
    NGEN = 250 #numero generazioni
    CXPB = 0.9 # probability of mating each individual at each generation 
    SELPARAM= 0.8 # 0.8
    TOURNPARAM= 0.9 # 0.9
    ELITEPARAM=0.3

    random.seed()
    toolbox = base.Toolbox()
    toolbox.register("attr_float", genind, BOUND_LOW, BOUND_UP, NDIM) #genera numeri
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float) #crea individui con attr_float
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) #ripete funzione individual
    pop = toolbox.population(n=MU)

    print(f"STOCK NAMES: {stocknames}",file=term)
    print(f"LISTA NOMI == DA AZIONI == STOCK AZIONI ({len(stocknames)} == {len(pop[0])} == {len(stockdf)})",file=term)
    print(f'LISTA AZIONI PREFERITE: {len(preftitle)} - {preftitle}',file=term)
    print(f'POP INIZIALE: {len(pop)}', end='',file=term)
    
    for MU in [48,100,200,500]:
        print(f'MU:{MU}', end=', ')
        for TOURNPARAM in [0.9,0.7,0.5]:
            print(f'TOURNPARAM:{TOURNPARAM}', end=', ')
            for SELPARAM in [0.8,0.6,0.4]:
                print(f'SELPARAM:{SELPARAM}', end=', ')
                for CXPB in [0.9,0.7,0.5]:
                    print(f'CXPB:{CXPB}', end=', ')
                    for NGEN in [10,25,50,100]:
                        print(f'NGEN:{NGEN}')
                        statslist=[]
                        listguadagno=[]
                        for tempo in range(1,maxtime+1): #arriva alla riga del csv time-1 min=1 max 153 per WEEK 738 per DAY (NUMERO DI RIGHE DA PRENDERE)
                            
                            # time.sleep()

                            def myfitness(ind):
                                listvar=[]
                                listrisk=[]
                                for i in range(len(stocknames)):
                                    totyield=0
                                    df=stockdf[i]
                                    listyeld=calcyield(df,"Close",tempo)
                                    listvar.append(np.var(listyeld))
                                    totyield += ind[i]*np.average(listyeld) #chiedere se usare np.mean()!!!!!!!!!!!
                                    # print(f"AVG: {np.average(listyeld)} totalyeld {totyield}")
                                for coppia in comb:
                                    x=coppia[0]
                                    y=coppia[1]
                                    df1=stockdf[x]
                                    df2=stockdf[y]
                                    listyeld1=calcyield(df1,"Close",tempo)
                                    listyeld2=calcyield(df2,"Close",tempo)
                                    cov=calccov(listyeld1,listyeld2,tempo)
                                    # print(f'{coppia},({individual[x]}{individual[y]}), {sum(individual)}')
                                    risk=calcrisk(ind[x]/sum(ind),ind[y]/sum(ind),listvar[x],listvar[y],cov) # crasha se sum(individual)=0
                                    listrisk.append(risk)
                                totrisk=sum(listrisk)
                                return (totrisk,totyield)

                            toolbox.register("evaluate", myfitness) #funzione fitness
                            toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0) #crossover func MODIFICATA CON INT
                            toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM) #mutation func MODIFICATA CON INT
                            toolbox.register("select", tools.selNSGA2) # funzione di selection

                            def main():

                                global pop
                                
                                if(len(stocknames)==len(pop[0])==len(stockdf)):

                                    data=str(pd.to_datetime(stockdf[0]["Date"][tempo-1]))[:-9] # -9 taglia i caratteri dei hh:mm:ss dalla stringa
                                    print(f"\n\n\n\n{tempo} ---- {data} ------------------------------------------------",file=term)
                                    print(f"\n\n\n\n{tempo} ---- {data} ------------------------------------------------",file=logb)
                                    print(f"{tempo} ---- {data}")


                                    print(f'\n%%%%%%%%PRIMA NSGA2: {len(pop)}',end='',file=term)

                                    pop,logbook =nsga2(pop)
                                    
                                    statslist.append(logbook)

                                    pickle.dump(listguadagno,open(f"guadagni_NGEN={NGEN}_CXPB={CXPB}_SELPARAM={SELPARAM}_TOURNPARAM={TOURNPARAM}_MU={MU}.dump","wb"))
                                    pickle.dump(statslist,open(f"stats_NGEN={NGEN}_CXPB={CXPB}_SELPARAM={SELPARAM}_TOURNPARAM={TOURNPARAM}_MU={MU}.dump","wb"))

                                    print(f'\n\n%%%%%%%%%DOPO NSGA2: {len(pop)}',end='',file=term)

                                    return

                                else:
                                    print(f"ERRORE: Lunghezza stocknames,pop,stockdf ({len(stocknames)}!={len(pop[0])}!={len(stockdf)})",file=term)

                            def nsga2(pop):

                                stats = tools.Statistics(lambda ind: ind.fitness.values)
                                stats.register("avg", np.mean, axis=0)
                                stats.register("std", np.std, axis=0)
                                stats.register("min", np.min, axis=0)
                                stats.register("max", np.max, axis=0)

                                logbook = tools.Logbook()
                                logbook.header = "gen", "evals", "std", "min", "avg", "max"

                                #  Valutare gli individui con un'idoneità non valida
                                if tempo>1:
                                    listguadagno.append([tempo,middle(stockdf,pop[0]),[i for i in pop[0]]])

                                invalid_ind = [ind for ind in pop if not ind.fitness.valid] #entra se valid = !False
                                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                                for ind, fit in zip(invalid_ind, fitnesses): #viene eseguito solo al primo for
                                    ind.fitness.values = fit

                                print(f'\n\n\t$$$ Prima di contazero e middle {len(pop)}',end='',file=term)
                                pop = [ind for ind in pop if (conta_azioni_possedute(ind)>=MINAZIONI and conta_azioni_possedute(ind)<=MAXAZIONI)] #cancella individui che hanno più di MAXZERI azioni a 0
                                pop = [ind for ind in pop if middle(stockdf,ind)<=BUDG] #cancella individui che hanno speso più di BUDG

                                print(f'\n\n\t$$$ dopo contazero e middle {len(pop)}',end='',file=term)

                                # Questo serve solo ad assegnare la distanza di affollamento agli individui non viene effettuata una vera e propria selezione
                                pop = toolbox.select(pop, int(len(pop)*SELPARAM))

                                record = stats.compile(pop) #compile() Applica ai dati della sequenza di input ogni funzione registrata e restituisce un dizionario. 
                                logbook.record(gen=0, evals=len(invalid_ind), **record)
                                print(logbook.stream,file=logb) #print header e gen0

                                print(f'\n\n\t$$$ Prima di gen {len(pop)}',file=term)

                                # Iniziare il processo generazionale
                                for gen in range(1, NGEN):
                                    
                                    print(f'\n\t\tiniz gen{gen} {len(pop)} ',file=term)

                                    elite=genelite(pop,PREF)
                                    elite = [toolbox.clone(ind) for ind in elite]

                                    # Vary the population            
                                    offspring = tools.selTournamentDCD(pop, closestMultiple(int(len(pop)*TOURNPARAM)))
                                    offspring = [toolbox.clone(ind) for ind in offspring]

                                    
                                    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):

                                        if random.random() <= CXPB:
                                            toolbox.mate(ind1, ind2)
                                        
                                        toolbox.mutate(ind1)
                                        toolbox.mutate(ind2)
                                        del ind1.fitness.values, ind2.fitness.values

                                    
                                    for ind1 in elite:
                                        for ind2 in offspring:

                                            if random.random() <= ELITEPARAM:
                                                toolbox.mate(ind1, ind2)
                        
                                            toolbox.mutate(ind1)
                                            toolbox.mutate(ind2)
                                            del ind1.fitness.values, ind2.fitness.values
                                    
                                    offspring = [ind for ind in offspring if (conta_azioni_possedute(ind)>=MINAZIONI and conta_azioni_possedute(ind)<=MAXAZIONI)] #cancella individui che hanno maxzeri azioni a 0
                                    offspring = [ind for ind in offspring if middle(stockdf,ind)<=BUDG] #cancella individua che hanno speso più di BUDG
                                

                                    # Valutare gli individual con un fitness non valido
                                    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                                    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                                    for ind, fit in zip(invalid_ind, fitnesses):
                                        ind.fitness.values = fit

                                    # Seleziona la popolazione di nuova generazione
                                    pop = toolbox.select(pop + offspring, MU)
                                    record = stats.compile(pop) #compile() Applica ai dati della sequenza di input ogni funzione registrata e restituisce un dizionario. 
                                    logbook.record(gen=gen, evals=len(invalid_ind), **record)
                                    print(logbook.stream,file=logb) #print riga gen
                                    
                                    print(f'\n\t\tfine gen {gen} {len(pop)}: ',file=term)


                                print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]),file=logb)

                                print(f'\n\t$$$$ Fine di nsgaII {len(pop)}',end='',file=term)

                                if tempo==1:
                                    listguadagno.append([tempo,middle(stockdf,pop[0]),[i for i in pop[0]]])

                                return pop ,logbook

                            def lucky(stockdf,ind):
                                lowtotal=0
                                for i in range(len(stockdf)):
                                        low = (stockdf[i]["Low"][tempo-1])*ind[i]
                                        # print(f"Low {low}")
                                        lowtotal+=low
                                # print(f"lowtotal: {lowtotal}")
                                return lowtotal

                            def murphy(stockdf,ind):
                                hightotal=0
                                for i in range(len(stockdf)):
                                        high = (stockdf[i]["High"][tempo-1])*ind[i]
                                        # print(f"High {high}")
                                        hightotal+=high
                                # print(f"hightotal: {hightotal}")
                                return hightotal

                            def calcyield(df,col,tempo): #individual è il numero di azioni possedute di quella azione è un indice di individual[]
                                yeld=[]
                                if tempo>=2:
                                    for i in reversed(range(1,len(df[col][:tempo]))):
                                        yeld.append(np.log(df[col][tempo-i]/df[col][tempo-i-1]))
                                        # print(i)
                                        # print(f'{df[col][tempo-i]} "+" {df[col][tempo-i-1]}')
                                        # print(f"{col} YIELD: {yeld}")
                                    return yeld
                                else: 
                                    # print("calcyield: tempo è minore di 2")
                                    yeld=[0]
                                    return yeld

                            def calccov(list1,list2,tempo):
                                if tempo>=3:
                                    cov=np.cov(list1,list2)
                                    cov=float(cov[1][0])
                                    # print(f"l1 {list1} l2 {list2} cov {cov}")
                                    return cov
                                else:
                                    return 0 

                            def calcrisk(az1,az2,var1,var2,cov): 
                                risk=(az1*var1)+(az2*var2)+(2*(az1*az2*cov)) 
                                return risk

                            def genelite(pop,pref):
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

                            def grafico(min,max):
                                fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 5))
                                # date=pd.to_datetime(stockdf[0]["Date"]) 
                                date=pd.to_datetime(stockdf[0]["Date"][:maxtime-1]) 
                                # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
                                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) # '%d-%m-%Y' ----- gca() get current axis, gcf() get current figure 
                                # plt.plot(date,valorimax,label="max",color="red")
                                ax[1,0].plot(date,[i[1] for i in min],label="min",color="blue")
                                ax[1,1].plot(date,[y[0] for y in max],label="max",color="red")
                                # plt.plot(date,list,label="max1",color="red")
                                # plt.plot(date,valorimin,label="min",color="green")
                                plt.title(f"Portfolio")
                                plt.xlabel("Data")
                                plt.xticks(rotation=20)
                                plt.ylabel("Valore")
                                plt.legend()
                                # plt.grid()
                                # plt.gcf().autofmt_xdate()
                                plt.show()   


                            if __name__ == "__main__":
                                main()

    # grafico(valorimin,[i[1] for i in listguadagno],valorimax)