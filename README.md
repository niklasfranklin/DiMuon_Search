# DiMuon Search

Python script for analyzing dimuon events in IceTray data frames.
Created in association with Harvard LPPC (2025)

### Legend:

examples: Example scripts for processing I3 files from L2->XLevel->DNN->BDT

jobbatch: The scripts for sumbmitting slurm job arrays.

pyscripts: All the python scripts for creating plots and writing icetray data to h5

repo: Folder containing all the necessary repositories

## Installs

### Prerequisites:

You'll need to have the IceTray environment already installed.
The version used for this project was py3-v4.3.0.

You'll also need the appropriate packages. Most come pre-packaged with IceTray, but some
specific versions of packages will be needed later. These can be installd in a virtual env (venv).
First, complete the setup.

### Setup:

Clone the DiMuon_Search Repo into your desired directory:

1. `cd /path/to/your/desired/directory`
2. `git clone https://github.com/DiMuon_Search`
3. `cd DiMuon_Search`

Next, setup the IceTray environment and activate your venv:

1. `ic_setup`
2. `icetray`
6. `virtualenv <venv_name>`
7. `export VENV_PATH=/path/to/your/venv_name`
8. `source $VENV_PATH/bin/activate`

Your `venv_name` will mainly be used for installing specific version of packages. the process-BDT scripts for example
require specific versions of h5py, sklearn-pypi etc...



