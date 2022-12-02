import matplotlib.pyplot as plt
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoode.algorithms import GDE3
from pymoode.survival import RankAndCrowding

problem = get_problem("tnk")
pf = problem.pareto_front()
print(pf)
gde3 = GDE3(
    pop_size=50, variant="DE/rand/1/bin", CR=0.5, F=(0.0, 0.9),
    survival=RankAndCrowding(crowding_func="pcd")
)

res = minimize(problem, gde3, ('n_gen', 200), seed=12)

fig, ax = plt.subplots(figsize=[6, 5], dpi=100)
ax.scatter(pf[:, 0], pf[:, 1], color="navy", label="True Front")
ax.scatter(res.F[:, 0], res.F[:, 1], color="firebrick", label="GDE3")
ax.set_ylabel("$f_2$")
ax.set_xlabel("$f_1$")
ax.legend()
fig.tight_layout()
plt.show()