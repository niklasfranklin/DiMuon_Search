# DiMuon Search

Python script for analyzing dimuon events in IceTray data frames.
Created in association with Harvard LPPC (2025)

### Legend:

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python script for creating plots and writing icetray data to h5

repo: Folder containing all the necessary repositories

## Installs

### Prerequisites:

You'll need to have the IceTray environment already installed.
The version used for this project was py3-v4.3.0.

You'll also need the appropriate packages. Most come pre-packaged with IceTray, but some
specific versions of packages will be needed later. These can be installd in a virtual env (venv).
First, complete the setup.

### Setup:

Setup the IceTray environment and activate your venv

1. `cd /path/to/your/desired/directory`

Next, setup the IceTray environment and activate your venv

1. `ic_setup`
2. `icetray`
6. `virtualenv <venv_name>`
7. `export VENV_PATH=/path/to/your/venv_name`
8. `source $VENV_PATH/bin/activate`



