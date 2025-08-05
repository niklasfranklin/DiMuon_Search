#!/bin/bash
#SBATCH -J BDT # A single job name for the array
#SBATCH -p shared # Partition; Choose whichever
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH --array 1 # Number of jobs; Once here

# 'Processes provided DNN reconstructed XLevel files through BDT.'

# 'To run, type into the terminal:'
# sbatch BDT_example.sh
# 'or copy line 14 into the terminal'

python process-BDT.py -c Config.txt -i 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_DNN.zst -o 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_BDT.zst
