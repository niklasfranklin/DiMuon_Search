# DiMuon Search

Python script for analyzing dimuon events in icetray data frames.

# Legend

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python script for creating plots and writing icetray data to h5

repo: Folder with all the necessary repositories

# Installs

Proccessing levels through BDT requires a specific environnment.
Set it up with the following:

1. `virtualenv <venv_name>`

Now setup the icetray environment and activate your venv

2. `ic_setup`
3. `icetray`
4. `export VENV_PATH=/path/to/your/venv_name`
5. `source $VENV_PATH/bin/activate`

These are the packages you'll need with their versions.


