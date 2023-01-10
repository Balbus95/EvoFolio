import pickle
import os
from deap import creator, base, tools

stats=pickle.load(open("stats.dump","rb"))
print(stats)

guadagni=pickle.load(open("guadagni.dump","rb"))
# print(guadagni[0])
for i in stats:
    print(i[1])
    