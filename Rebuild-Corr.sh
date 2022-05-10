#!/bin/bash
#SBATCH --partition=scopion2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

export OMP_NUM_THREADS=8

PATH=/home/liusf/anaconda3/bin:${PATH}
source /home/liusf/intel/bin/compilervars.sh intel64

date
python Rebuild-Corr.py
echo -e "\ndone.\n\n"
date


