# To run this use
#
#     $ docker load < $(nix-build docker.nix) && docker run -it fipy-docker:latest

let
  pkgs = import (builtins.fetchGit {
      url = "https://github.com/NixOS/nixpkgs.git";
      rev = "0cebf41b6683bb13ce2b77bcb6ab1334477b5b29"; # 20.09-alpha
      ref = "release-20.09";
    }) { };
  lib = pkgs.lib;
  USER = "main";

  ## files to copy into the user's home area in container
  files_to_copy = [ ./benchmark8a.py ./params8a.yaml ];

  ## functions necessary to copy files to USER's home area
  ## is there an easier way???
  filetail = path: lib.last (builtins.split "(/)" (toString path));
  make_cmd = path: "cp ${path} ./home/${USER}/${filetail path}";
  copy_cmd = paths: builtins.concatStringsSep ";\n" (map make_cmd paths);
in
  pkgs.dockerTools.buildImage {
    name = "fipy-docker";
    tag = "latest";

    contents = [ (import ./default.nix { inherit pkgs; }) ] ++ [
      pkgs.bash
      pkgs.busybox
      pkgs.coreutils
      pkgs.openssh
      pkgs.bashInteractive
    ];

    runAsRoot = ''
      #!${pkgs.stdenv.shell}
      ${pkgs.dockerTools.shadowSetup}
      groupadd --system --gid 65543 ${USER}
      useradd --system --uid 65543 --gid 65543 -d / -s /sbin/nologin ${USER}
    '';

    extraCommands = ''
      mkdir -m 1777 ./tmp
      mkdir -m 777 -p ./home/${USER}
    '' + copy_cmd files_to_copy;

    config = {
      Cmd = [ "bash" ];
      User = "main";
      Env = [
        "OMPI_MCA_plm_rsh_agent=${pkgs.openssh}/bin/ssh"
        # "PETSC_DIR=${pkgs.petsc.out}"
      ];
      WorkingDir = "/home/${USER}";
    };
  }
