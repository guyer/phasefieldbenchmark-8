#!/bin/bash
# invoke with
# $ sbatch --ntasks=16 problem8c.sh <env> <solver> <tag> [args]

#SBATCH --partition rack3             # -p, partition
#SBATCH --time 12:00:00               # -t, time (hh:mm:ss or dd-hh:mm:ss)
#SBATCH --nodes=1                     # -N, total number of machines
#SBATCH --ntasks=64                   # -n, 64 MPI ranks per Opteron machine
#SBATCH -J Problem-8c
#SBATCH -D /data/guyer/CHiMaD/phase_field/phasefieldbenchmark-8

CONDAENV=$1
SOLVER=$2
TAG=$3

shift
shift
shift

source /data/guyer/miniconda3/bin/activate $CONDAENV

OMP_NUM_THREADS=1 FIPY_SOLVERS=$SOLVER mpiexec -n 1 smt run --tag $TAG -n $SLURM_NTASKS --main benchmark8c.py params8c.yaml "$@"

