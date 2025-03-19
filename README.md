Important files:
 - `environment.yaml`: The environment used to run dscim. I install this using conda.
 - `configs/dummy_config.yaml`: Config that is used to save file paths and run dscim.
 - `file_creation.ipynb`: Creates all of the necessary inputs according to the config paths.
 - `menu.ipynb`: Generates a dscim menu that you can play with.
 - `run_integration_result.py`: This is the type of run script that I use to run the integration results.

General setup:
1. Create the conda environment with `conda env create -f environment.yaml`.
2. Run through `file_creation.ipynb`. Feel free to tweak various coordinate values to see where stuff breaks.
3. Run at least the `reduce_damages` step of `run_integration_result.py`. I've commented out some code that hasn't been implemented in this play example.
4. Using either `menu.ipynb` or `run_integration_result.py`, play with dscim!
