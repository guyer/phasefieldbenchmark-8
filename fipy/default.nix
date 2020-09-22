# Petsc currently needs some work. Petsc4py is passing all the tests,
# but giving a "core dumped" error when run as the solver suite for
# FiPy.  Maybe try some of the "Firedrake" settings and override the
# Nixpkgs expression.
#
# Nixpkgs: https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/libraries/science/math/petsc/default.nix
#
# Firedrake: https://git.sharcnet.ca/nix/nixpkgs-sharcnet/-/blob/master/firedrake/petsc.nixxs

{pkgs ? import <nixpkgs> {} }:
let
    pythonPackages = pkgs.python3Packages;
in
  pkgs.buildEnv rec {
    name = "fipy-env";
    paths = [(pkgs.python3.withPackages (ps: with ps; [
      jupyter
      pip
      fipy
      pyyaml
      # pkgs.petsc
      cython
      pkgs.openmpi
      pkgs.hdf5
      # (callPackage ./petsc4py.nix {})
      python
      pkgs.bash
    ]))];

    # shellHook = ''
    #   jupyter nbextension install --py widgetsnbextension --user
    #   jupyter nbextension enable widgetsnbextension --user --py

    #   SOURCE_DATE_EPOCH=$(date +%s)
    #   export PYTHONUSERBASE=$PWD/.local
    #   export USER_SITE=`python -c "import site; print(site.USER_SITE)"`
    #   export PYTHONPATH=$PYTHONPATH:$USER_SITE
    #   export PATH=$PATH:$PYTHONUSERBASE/bin

    #   export PETSC_DIR="${petsc.out}"

    # '';
  }
