# FiPy Nucleation Benchmark Example

This directory contains the input files to solve [PFHub benchmark
8a](https://pages.nist.gov/pfhub/benchmarks/benchmark8.ipynb/), which
is a phase field nucleation problem, using the [FiPy] PDE solver.

This is a sample of the all the results necessary to produce the FiPy
data for the [nucleation paper]. See [this repository] for the
complete set of input files necessary.

The FiPy setup is currently far from complete. See the issues that are
still broken for more details of problems that still need to be
addressed.

## Installation using Docker

[Install Docker](https://docs.docker.com/get-docker/) on your platform
and check that `docker run hello-world` runs. To download and run the
FiPy nucleation benchmark container use,

    $ docker run -it wd15/fipy-nucleation:latest

This will drop you into a bash shell with the necessary dependencies
to run FiPy. See the [Usage section](#usage) for more details.

Note that there is no need to clone this repository to use the Docker
installation.

## Installation using Conda

[Install Conda][conda-install], clone this repository and from the
`fipy` directory,

    $ conda env create -f environment.yml
    $ conda activate fipy-nucleation

This will drop you into an environment with the necessary dependencies
to run FiPy. See the [Usage section](#usage) for more details.

## Installation using Nix

Install Nix, clone this repository and from the `fipy` directory,

    $ nix-shell

This will drop you into an environment with the necessary dependencies
to run FiPy. See the [Usage section](#usage) for more details.

## <a name="usage"> Usage </a>

Currently, the only FiPy implementation is for benchmark 8a. Assuming
that you have followed the installation instructions above then run

    $ python benchmark8a.py params8a.yaml

from the `fipy` directory. The output data will be written to the
`data` directory.

## Build the Docker Instance

To build the Docker instance use,

    $ docker load < $(nix-build docker.nix)

or

    $ docker load < $(nix-build docker.nix) && docker run -it wd15/fipy-nucleation:latest

to build and run.

[FiPy]: https://www.ctcms.nist.gov/fipy/
[conda-install]: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
[nucleation paper]: ...
[this repository]: https://github.com/guyer/phasefieldbenchmark-8
