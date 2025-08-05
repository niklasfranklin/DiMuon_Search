#!/bin/bash
#SBATCH -J DNN # A single job name for the array
#SBATCH -c 8 # Number of cores
#SBATCH -p shared # Partition; Choose whichever
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH --array 1 # Number of jobs; Once here

# 'Processes provided XLevel files through DNN reconstruction.'

# 'To run, type into the terminal:'
# sbatch DNN_example.sh
# 'or copy line 15 into the terminal'

python process-DNN.py -c Config.txt -i 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_XLevel.zst -o 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_DNN.zst

# 'This will spit out the XLevel file as well as a log of cuts being made 'L3_cuts', ignore the cuts.'


