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


ATTENTION: In `distributed` launch_mode, Sumatra *must* be invoked with::

  mpiexec -n 1 smt run -n 2 --main benchmark8a.py params.yaml

to keep MPICH happy.
