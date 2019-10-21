#!/bin/bash
#SBATCH --partition rack3             # -p, partition
#SBATCH --time 12:00:00               # -t, time (hh:mm:ss or dd-hh:mm:ss)
#SBATCH --nodes=1                     # -N, total number of machines
#SBATCH --ntasks=64                   # -n, 64 MPI ranks per Opteron machine
#SBATCH -J 8d
#SBATCH -D /data/guyer/CHiMaD/phase_field/phasefieldbenchmark-8

. /data/guyer/miniconda3/etc/profile.d/conda.sh

conda activate fipy

export OMP_NUM_THREADS=1
/data/guyer/miniconda3/envs/fipy/bin/mpiexec -n 1 smt run -n $SLURM_NTASKS --main benchmark8d.py params8d.yaml "$@"
