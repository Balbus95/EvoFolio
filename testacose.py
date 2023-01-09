import pickle
import os
from deap import creator, base, tools

# stats=pickle.load(open("stats.pickle","rb"))
# print(stats)

guadagni=pickle.load(open("guadagni.pickle","rb"))
# print(guadagni[0])
for i in guadagni:
    print(i[1])
    