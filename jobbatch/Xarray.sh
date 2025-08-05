#!/bin/bash
#SBATCH -J X # A single job name for the array
#SBATCH -p sapphire # Partition
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH -o /n/netscratch/arguelles_delgado_lab/Everyone/nfranklin/DiMuons/logs/X_%A_%a.out # Standard output
#SBATCH -e /n/netscratch/arguelles_delgado_lab/Everyone/nfranklin/DiMuons/logs/X_%A_%a.err # Standard error
#SBATCH --array 1-5 # Number of jobs; Five here, change to number of files total

# Processes provided L2 files into XLevel (L3). Specify if they are volume or ranged injection.

python /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/repo/MEOWS/processing/process-XLevel.py -i /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/miaochenjin/DBSearch/SIREN_outputs/0723_NuMu_charm_astro_ranged_1e2-1e6/simulation/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_L2Level.zst -o /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/XLevel/xfiles_ranged/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_1_XLevel_isMuonFilter.zst --ice_model spice_ftp-v3m --gcdfile /n/holylfs05/LABS/arguelles_delgado_lab/Lab/meows_dnn/mc/Nominal/GeoCalibDetectorStatus_IC86.AVG_Pass2_SF0.99.i3.gz --spline_path /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/repo/MEOWS/resources/paraboloidCorrectionSpline.dat
