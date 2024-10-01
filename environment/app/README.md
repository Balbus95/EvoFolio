# EvoPortfolio 
More information is available in the article: [EvoPortfolio - Research Article](https://rdcu.be/dI8ZF)

### Table of Contents
- [Installation](#installation)
- [Run](#run)
- [Parameters](#parameters)

## Installation
The latest version can be cloned with the following command:

```bash
`git clone --recurse-submodules https://github.com/Balbus95/EvoPortfolio.git`
```

<details><summary><b>Notes to manual installation of my custom DEAP submodule</b></summary>
  
  Use one of the following commands to install the custom DEAP library: 
  
  ```bash
  pip install .\deap --use-pep517
  ```
  
  Or:
  
  ```bash
  pip install ./deap
  ```
</details>

### Create a Virtual Environment:
Use the following command to create a virtual environment:

```bash
python3 -m venv venv
```

Note: to activate and deactivate the virtual environment, use `source env/bin/activate` and `deactivate` on Linux/MacOS, or `venv\Scripts\activate` and `deactivate` on Windows.


### Install Other Dependencies

```bash
`pip install -r requirements.txt`
```

## Run

To run the main script:

```bash
` python evoportfolio.py `
```

In the current version, the script to use is:

```bash
` python '.\final hybrid.py' `
```

### Other scripts

You can run other scripts in the same way.

- Run the `loadfile.py` script to view graphs of the `.dump` files created by the main script.

- Run `stockToPDF.py` to generate PDFs of the trend graphs for each stock. Modify the `PATHCSVFOLDER` path (default: `./stock/WEEK`) if necessary. PDFs will be saved in the `stockToPDF_out` folder.

## Parameters

### Default Parameters of the Scripts

```python
MINAZIONI, MAXAZIONI= 10, 14 # min and max number of different stocks that a portfolio can hold
BUDG = 1000000 # initial budget of portfolios (USD$)
BOUND_LOW, BOUND_UP = 0, BUDG # min and max number of equal stock that a portfolio can hold
NDIM = len(stockdf) # portfolio size (number of stock's files)
MAXTIME=24 # maximum csv row to read, the row is the date in the csv
ELITEPARAM=0.3 # elite parameter, e.g. 0.3 selects 30% of the pop
```

**Note**: the parameters below are overwritten by the `for` loop. If you want to change them, edit them in `evoportfolio.py`.

```python
MU = 100 # population size, number of individuals in the population.
TOURNPARAM= 0.9 # tournament parameter, e.g. 0.9 selects 90% of the pop
SELPARAM= 0.8 # NSGA-II selection parameter, e.g. 0.8 selects 80% of the pop
CXPB = 0.9 # probability of mating each individual at each generation 
NGEN = 250 # number of generation of nsga2
```

### Default Paths

To change the input and output paths, edit the following parameters in `evoportfolio.py` and `loadfile.py`:

```python
# Input - `evoportfolio.py`
PATHCSVFOLDER = "./stock/WEEK/" # path of portfolio stock folder
# Output - `loadfile.py`
PATHLOGBMONFOLDER = "./output/mensile/logbook/" # path where saves monthly `Logb_x` files
PATHGUADMONFOLDER = "./output/mensile/guadagni/" # path where saves monthly `Guad_x` files
PATHLOGBTRIFOLDER = "./output/trimestrale/logbook/" # path where saves monthly `Logb_x` files
PATHGUADTRIFOLDER = "./output/trimestrale/guadagni/" # path where saves trimestral `Guad_x` files
```
