# DiMuon Search

Python script for analyzing dimuon events in IceTray data frames.

## Legend

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python script for creating plots and writing icetray data to h5

repo: Folder containing all the necessary repositories

# Installs

## Prerequisites

You'll need to have the IceTray environment already installed.

To access the contents of the repository, you'll need to clone it into your workspace using the command:

1. `cd /your/favorie/directory`
2. `git clone https://github.com/DiMuon_Search`

Some scripts like proccessing levels through BDT requires a specific environnment.
You can set up a virtual one with the following:

3. `virtualenv <venv_name>`

Now setup the IceTray environment and activate your venv

4. `ic_setup`
5. `icetray`
6. `export VENV_PATH=/path/to/your/venv_name`
7. `source $VENV_PATH/bin/activate`

Next you'll need the appropriate packages, 



