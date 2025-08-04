# Legend

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python script for creating plots and writing icetray data to h5

repo: Folder with all the necessary repositories

# Installs

Proccessing levels through BDT requires a specific environnment.
Set it up with the following:

1. create a python virtual env (venv)
2. `virtualenv <venv_name>`

Now setup the icetray environment and activate your venv

6. `ic_setup`
7. `icetray`
8. `export VENV_PATH=/path/to/your/venv_name`
9. `source $VENV_PATH/bin/activate`


