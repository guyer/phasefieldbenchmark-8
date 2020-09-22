# Petsc currently needs some work. Petsc4py is passing all the tests,
# but giving a "core dumped" error when run as the solver suite for
# FiPy.  Maybe try some of the "Firedrake" settings and override the
# Nixpkgs expression.
#
# Nixpkgs: https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/libraries/science/math/petsc/default.nix
#
# Firedrake: https://git.sharcnet.ca/nix/nixpkgs-sharcnet/-/blob/master/firedrake/petsc.nixxs

let
    pkgs = import (builtins.fetchGit {
      url = "https://github.com/NixOS/nixpkgs.git";
      rev = "0cebf41b6683bb13ce2b77bcb6ab1334477b5b29"; # 20.09-alpha
      ref = "release-20.09";
    }) { };
in
  pkgs.mkShell rec {
    name = "fipy-shell";
    buildInputs = [ (import ./default.nix { inherit pkgs; }) ];
    # buildInputs = (import ./default.nix { inherit pkgs; }).nothin;
    # propagatedBuildInputs = [ (import ./default.nix { inherit pkgs; }) ];
    # nativeBuildInputs = propagatedBuildInputs;

    shellHook = ''

      jupyter nbextension install --py widgetsnbextension --user
      jupyter nbextension enable widgetsnbextension --user --py

      SOURCE_DATE_EPOCH=$(date +%s)
      export PYTHONUSERBASE=$PWD/.local
      export USER_SITE=`python -c "import site; print(site.USER_SITE)"`
      export PYTHONPATH=$PYTHONPATH:$USER_SITE
      export PATH=$PATH:$PYTHONUSERBASE/bin
      export OMPI_MCA_plm_rsh_agent=/usr/bin/ssh

      export PETSC_DIR="${pkgs.petsc.out}"

    '';
  }
