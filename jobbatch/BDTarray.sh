#!/bin/bash
#SBATCH -J BDT # A single job name for the array
#SBATCH -p sapphire # Partition; Choose whichever
#SBATCH --mem 8000 # Memory request (8Gb)
#SBATCH -t 0-2:00 # Maximum execution time (D-HH:MM)
#SBATCH -o /n/netscratch/arguelles_delgado_lab/Everyone/nfranklin/BDT/logs/%A_%a.out # Standard output; Change to your log dir
#SBATCH -e /n/netscratch/arguelles_delgado_lab/Everyone/nfranklin/BDT/logs/%A_%a.err # Standard error; Change to your log dir
#SBATCH --array 1-5 # Number of jobs; Five here, change to number of files total

# Processes provided DNN reconstructed XLevel files through BDT. Specify if they are volume or ranged injection.

python /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/repo/MEOWS/processing/legacy/process-BDT.py -c /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/Config.txt -i /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/DNN/dnnfiles_ranged/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_${SLURM_ARRAY_TASK_ID}_DNN.zst -o /n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/BDT/bdtfiles_ranged/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_${SLURM_ARRAY_TASK_ID}_BDT.zst
