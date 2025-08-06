#!/bin/bash
#SBATCH -J BDT # A single job name for the array
#SBATCH -p shared # Partition; Choose whichever
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH --array 1 # Number of jobs; Once here

# 'This script filters event frames in an I3 file and keep frames that contain DiMuon Events.'
# 'This was specifically used for L2, but should work for others.'

# 'To run, type into the terminal:'
# sbatch DiMuon_example.sh
# 'or copy line 15 into the terminal'

python filter_DiMuon.py -i 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_L2Level.zst -o 0723_NuMu_charm_astro_ranged_1e2-1e6_DiMuon_seed_1_L2Level.zst

# 'While in the IceTray environment, use the 'dataio-shovel' command to look at the contents of the new I3 file.'