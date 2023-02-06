# EvoPortfolio 
### Table of Contents
- [Installation](#installation)
- [Run](#run)
- [Parameters](#parameters)
## Installation
The latest version can be installed with
```bash
`git clone --recurse-submodules https://github.com/Balbus95/EvoPortfolio.git`
```
#### For Windows:
Install the custom DEAP library
```bash
`pip install .\deap --use-pep517` or with `pip install .\deap`
```
#### For Linux/MacOS:
Install the custom DEAP library
```bash
`pip install ./deap --use-pep517` or with `pip install ./deap`
```
<details><summary><b>Notes to set up a libraries for VSCode on Linux/MacOS</b></summary>
<p>

To set up a libraries for VSCode on Linux/MacOS you can use
```bash
`python3 -m venv env`
```
Note: to enable and disable a virtual environments use `source env/bin/activate` and `deactivate`
</p>
</details>

### Install other dependency libraries
```bash
`pip install matplotlib`
`pip install pandas`
`pip install numpy`
```
## Run
```bash
`python evoportfolio.py`
```
### Other scripts
in the same way

Run the `loadfile.py` script to see graphs of the .dump files created with the main script

Run `stockToPDF.py` to generate PDFs of the trend graphs for each stock (change the `PATHCSVFOLDER` path), default path is `./stock/WEEK`, PDFs are saved in the `stockToPDF_out` folder

## Parameters
<b>Default parameters of scripts</b> 
```python
MINAZIONI, MAXAZIONI= 10, 14 # min and max number of different stocks that a portfolio can hold
BUDG = 1000000 # initial budget of portfolios (USD$)
BOUND_LOW, BOUND_UP = 0, BUDG # min and max number of equal stock that a portfolio can hold
NDIM = len(stockdf) # portfolio size (number of stock's files)
MAXTIME=24 # maximum csv row to read, the row is the date in the csv
ELITEPARAM=0.3 # elite parameter, e.g. 0.3 selects 30% of the pop
```
##### Note: these below are overwritten by the `for`, if you want to change them, edit them in the `evoportfolio.py`
```python
MU = 100 # population size, number of individuals in the population.
TOURNPARAM= 0.9 # tournament parameter, e.g. 0.9 selects 90% of the pop
SELPARAM= 0.8 # NSGA-II selection parameter, e.g. 0.8 selects 80% of the pop
CXPB = 0.9 # probability of mating each individual at each generation 
NGEN = 250 # number of generation of nsga2
```
<b>Default path</b> for input and output, if you want to change them, edit them in the `evoportfolio.py` and in `loadfile.py`
```python
# Input - `evoportfolio.py`
PATHCSVFOLDER = "./stock/WEEK/" # path of portfolio stock folder
# Output - `loadfile.py`
PATHLOGBMONFOLDER = "./output/mensile/logbook/" # path where saves monthly `Logb_x` files
PATHGUADMONFOLDER = "./output/mensile/guadagni/" # path where saves monthly `Guad_x` files
PATHLOGBTRIFOLDER = "./output/trimestrale/logbook/" # path where saves monthly `Logb_x` files
PATHGUADTRIFOLDER = "./output/trimestrale/guadagni/" # path where saves trimestral `Guad_x` files
```
