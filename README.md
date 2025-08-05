# DiMuon Search

Python script for analyzing dimuon events in icetray data frames.

# Legend

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python script for creating plots and writing icetray data to h5

repo: Folder with all the necessary repositories

# Installs

To access the contents, you'll need to clone the repository into your workspace using the command:

1. cd /your/favorie/directory
2. `git clone https://github.com/DiMuon_Search`

Proccessing levels through BDT requires a specific environnment.
Set it up with the following:

3. `virtualenv <venv_name>`

Now setup the icetray environment and activate your venv

4. `ic_setup`
5. `icetray`
6. `export VENV_PATH=/path/to/your/venv_name`
7. `source $VENV_PATH/bin/activate`

Next you'll need the appropriate packages,



