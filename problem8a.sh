#!/bin/bash
#SBATCH --partition rack3             # -p, partition
#SBATCH --time 12:00:00               # -t, time (hh:mm:ss or dd-hh:mm:ss)
#SBATCH --nodes=1                     # -N, total number of machines
#SBATCH --ntasks=16                   # -n, 64 MPI ranks per Opteron machine
#SBATCH -J Problem-8a
#SBATCH -D /data/guyer/CHiMaD/phase_field/phasefieldbenchmark-8

. /tmp/guyer/miniconda2/etc/profile.d/conda.sh

conda activate cluster_fipy

export OMP_NUM_THREADS=1
/tmp/guyer/miniconda2/envs/cluster_fipy/bin/mpiexec -n 1 smt run -n $SLURM_NTASKS --main benchmark8a.py params8a.yaml "$@"
