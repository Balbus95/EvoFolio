# EvoFolio 
More information is available in the article: [EvoFolio - Research Article](https://rdcu.be/dI8ZF)

### Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Run](#run)
- [Parameters](#parameters)

## Description
EvoFolio is a project that implements the NSGA-II algorithm applied to portfolio optimization. It computes different financial metrics (like yield and risk) based on stock data, and allows visualization of the generated data.

## Installation
The latest version can be cloned with the following command:

```bash
git clone --recurse-submodules https://github.com/Balbus95/EvoFolio.git
```

### Create a Virtual Environment (Optional but Recommended):
Use the following command to create a virtual environment:

```bash
python3 -m venv venv
```

Note: to activate and deactivate the virtual environment, use `source venv/bin/activate` and `deactivate` on Linux/MacOS, or `venv\Scripts\activate` and `deactivate` on Windows.

### Install Dependencies

Dependencies, including the custom DEAP submodule, can be installed by running:

```bash
pip install -r requirements.txt
```

<details><summary><b>Notes on manual installation of the custom DEAP submodule</b></summary>
  
  In case you need to install the custom DEAP library manually, use one of the following commands: 
  
  ```bash
  pip install .\deap --use-pep517
  ```
  
  Or:
  
  ```bash
  pip install ./deap
  ```
</details>

## Run

To run the main optimization script:

```bash
python "final hybrid.py"
```

### Other scripts

You can run other utility scripts in the same way:

- **`loadfile.py`**: Run this script to open a Tkinter GUI to view and plot graphs of the `.dump` files created by the main script. It supports both monthly and trimestral outputs.
- **`stockToPDF.py`**: Run this script to generate PDFs of the trend graphs (close prices) for each stock. PDFs will be saved in the `stockToPDF_out` folder.

## Parameters

### Default Parameters of the Main Script (`final hybrid.py`)

The following parameters can be modified directly at the beginning of `final hybrid.py`:

```python
MINAZIONI, MAXAZIONI= 10, 14 # min and max number of different stocks that a portfolio can hold
BUDG = 1000000 # initial budget of portfolios (USD$)
BOUND_LOW, BOUND_UP = 0, BUDG # min and max number of equal stock that a portfolio can hold
NDIM = len(stockdf) # portfolio size (number of stock's files)
SELPARAM= 0.8 # NSGA-II selection parameter, e.g. 0.8 selects 80% of the pop
CXPB = 0.9 # probability of mating each individual at each generation 
ELITECXPB=0.3 # probability of mating with an elite
MAXTIME=24 # maximum csv row to read, the row is the date in the csv
```

**Note**: the parameters below might be overwritten by a loop in the script. To change them, modify the loop definitions near the bottom of `final hybrid.py`:

```python
MU = 250 # population size, number of individuals in the population.
TOURNPARAM= 0.9 # tournament parameter, e.g. 0.9 selects 90% of the pop
NGEN = 50 # number of generation of nsga2
```

### Default Paths

The input and output folder paths are set by default to work seamlessly on both Windows and Unix systems. If you need to change them, look for `PATHCSVFOLDER`, `PATHLOGBMONFOLDER`, etc., in the scripts:

- **Inputs**: Inside `final hybrid.py`, `loadfile.py` and `stockToPDF.py`. Default stock data path is `./stock/WEEK`.
- **Outputs**: Handled in `final hybrid.py` and `loadfile.py`. Default output paths are `./output/mensile/...` and `./output/trimestrale/...`.


---

## ☕ Support

If my work was useful, a coffee is always welcome!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/balbus95)
