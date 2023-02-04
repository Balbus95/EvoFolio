# EvoPortfolio 

The latest version can be installed with
`git clone --recurse-submodules https://github.com/Balbus95/EvoPortfolio.git`

For Windows:
Install the custom DEAP library with
`pip install .\deap --use-pep517` or with `pip install .\deap`

For Linux/MacOS:
To set up a libraries for VSCode on Linux/MacOS you can use
`python3 -m venv env`
Note: to enable and disable a virtual environments use
`source env/bin/activate` and `deactivate` 
Install the custom DEAP library with 
`pip install ./deap --use-pep517` or with `pip install ./deap`

Install other dependency libraries with
`pip install matplotlib`
`pip install pandas`
`pip install numpy`

Run the main script with `python evoportfolio.py`

in the same way
Run the `loadfile.py` script to see graphs of the .dump files created with the main script

Run `stockToPDF.py` to generate PDFs of the trend graphs for each stock (change the `PATHCSVFOLDER` path), default path is `./stock/WEEK`, PDFs are saved in the `stockToPDF_out` folder