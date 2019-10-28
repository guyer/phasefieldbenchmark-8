# Phase Field Benchmark 8

## Overview

[FiPy](https://www.ctcms.nist.gov/fipy) implementation of 
Phase Field Benchmark #8 ("Benchmark problems for nucleation - Tamás 
Pusztai - September 25, 2019")

## Sumatra

```
smt init --store datreant://.smt/records benchmark8
smt configure --executable python --addlabel parameters \
  --labelgenerator uuid --launch_mode distributed \
  --pfi_path /Users/guyer/anaconda/envs/fipy/bin/pfi.py
```

Results are stored in the `Data/` directory using a customized
[sumatra](http://neuralensemble.org/sumatra/)
on branch `datreant_store` @ 9d41e9e.

```
$ smt info
Project name        : benchmark8
Default executable  : Python (version: 2.7.15) at /Users/guyer/anaconda/envs/fipy/bin/python
Default repository  : GitRepository at /Users/guyer/Documents/research/CHiMaD/phase_field/phasefieldbenchmark-8
Default main file   : None
Default launch mode : distributed (n=1, mpiexec=/Users/guyer/anaconda/envs/fipy/bin/mpiexec, hosts=[])
Data store (output) : /Users/guyer/Documents/research/CHiMaD/phase_field/phasefieldbenchmark-8/Data
.          (input)  : /
Record store        : Record store using the datreant package (database file=.smt/records)
Code change policy  : error
Append label to     : parameters
Label generator     : uuid
Timestamp format    : %Y%m%d-%H%M%S
Plug-ins            : []
Sumatra version     : 0.8dev
```


ATTENTION: In `distributed` launch_mode, Sumatra *must* be invoked with
```
mpiexec -n 1 smt run -n <n> --main benchmark8a.py params.yaml
```
to keep MPICH happy.


## CTCMS Cluster Issues

NOTE: default mpirun on ruth and cluster nodes

### Case 1

Launching with
```
/tmp/guyer/miniconda2/envs/cluster_fipy/bin/mpiexec -n 1 smt run -n $SLURM_NTASKS --main benchmark8b.py params8b.yaml "$@"
```
produced (Andrew fixed this[*])
```
[mpiexec@r001] HYDU_create_process (utils/launch/launch.c:75): execvp error on file srun (No such file or directory)
```

This error message is supposed to mean that `mpiexec` is trying to call 
something (`srun`) that can't be found, but `srun` calls `mpiexec`, not 
the other way around? 

Sumatra doesn't call `srun`. 

Taking `smt` out of it altogether doesn't help.

[*] Andrew fixed this by installing `srun` on `r001`.  Apparently *his*
`mpiexec` needs to be rebuilt somehow to invoke this `srun`, but the
`mpiexec` I get from conda is A-OK. Installing on other nodes will require 
taking down their slurm queues, so probably won't happen until site-wide 
shutdown over 25-27 OCT 2019.

### Case 2

Launching with
```
/usr/bin/mpirun -n 1 smt run -n $SLURM_NTASKS --main benchmark8b.py params8b.yaml "$@"
```
produces
```
**********************************************************

Open MPI does not support recursive calls of mpiexec

**********************************************************
```

This is because `/usr/bin/mpirun` is from OpenMPI and the error message is 
pretty descriptive. For that `mpirun`, Sumatra should be invoked with 
```
smt run -n <n> --main benchmark8a.py params.yaml
```
but then the `mpirun` invoked by `DistributedLaunchMode` is the wrong one.
???What happens???

### Case 3

Launching with default `mpiexec`
```
mpiexec -n 1 smt run -n $SLURM_NTASKS --main benchmark8b.py params8b.yaml "$@"
```
(more specifically
```python
>>> mpi4py.MPI.COMM_SELF.Spawn("/tmp/guyer/miniconda2/envs/cluster_fipy/bin/python",
...                            args=["/tmp/guyer/miniconda2/envs/cluster_fipy/bin/pfi.py"])
```
produces
```
[mpiexec@r001] match_arg (utils/args/args.c:159): unrecognized argument pmi_args
[mpiexec@r001] HYDU_parse_array (utils/args/args.c:174): argument matching returned error
[mpiexec@r001] parse_args (ui/mpich/utils.c:1596): error parsing input array
[mpiexec@r001] HYD_uii_mpx_get_parameters (ui/mpich/utils.c:1648): unable to parse user arguments
[mpiexec@r001] main (ui/mpich/mpiexec.c:149): error parsing parameters
```

### Upshot

Launch with
```
/tmp/guyer/miniconda2/envs/cluster_fipy/bin/mpiexec -n 1 smt run -n $SLURM_NTASKS --main benchmark8b.py params8b.yaml "$@"
```
and ensure that `srun` is installed on cluster nodes.

### SlurmMPILaunchMode

Would `SlurmMPILaunchMode` take care of queuing *and* get rid of the slurm 
script? Needs `salloc` installed on cluster nodes.

No. `SlurmMPILaunchMode` does work, but it doesn't really "queue". The
`smt` process remains running, so it's not useful for fire-and-forget.
