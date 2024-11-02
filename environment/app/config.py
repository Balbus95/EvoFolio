#### Default parameters 
MINAZIONI, MAXAZIONI= 1, 5 # Min and max number of different stocks that a portfolio can hold
BUDG = 1000000 # Initial budget of portfolios
BOUND_LOW, BOUND_UP = 0, BUDG # Min and max number of equal stock that a portfolio can hold
SELPARAM= 0.8 # NSGA-II selection parameter, e.g. 0.8 selects 80% of the pop
CXPB = 0.9 # Probability of mating each individual at each generation 
ELITECXPB=0.3 # Probability of mating with an elite

#### These below are overwritten by the next "for", edit or remove them
TOURNPARAM= 0.9 # Tournament parameter, e.g. 0.9 selects 90% of the pop
MU = 20 # Population size, number of individuals in the population.
NGEN = 10 # Number of generation of nsga2

# Parametri che subiscono modifiche runtime
MAXTIME=50 # Maximum csv row to read, the row is the date in the csv, in this case using /stock/WEEK each csv row equals one week, 24 is 6 months, comment to use the maximum length of the csv
tempo=1
NDIM=5 # dimensione in termini di capienza del portfolio dove a quanti azioni ha disponibili l'individio, deve essere quanti sono i file csv dei titoli # INUTILE ORA (final.py:73)
