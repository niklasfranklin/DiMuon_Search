#!/bin/bash
#SBATCH -J X # A single job name for the array
#SBATCH -p shared # Partition
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH --array 1# Number of jobs; Once here

# 'Processes provided L2 files into XLevel (L3)'

# 'To run, type into the terminal:'
# sbatch XLevel_example.sh
# 'or copy line 14 into the terminal'

python process-XLevel.py -i 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_L2Level.zst -o 0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_XLevel.zst --ice_model spice_ftp-v3m --gcdfile /n/holylfs05/LABS/arguelles_delgado_lab/Lab/meows_dnn/mc/Nominal/GeoCalibDetectorStatus_IC86.AVG_Pass2_SF0.99.i3.gz --spline_path /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/repo/MEOWS/resources/paraboloidCorrectionSpline.dat

# 'This will spit out the XLevel file as well as a log of cuts made; 'L3_cuts', ignore the cuts.'
