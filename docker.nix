# To run this use
#
#     $ docker load < $(nix-build docker.nix) && docker run -it fipy-docker:latest

let
  pkgs = import (builtins.fetchGit {
      url = "https://github.com/NixOS/nixpkgs.git";
      rev = "0cebf41b6683bb13ce2b77bcb6ab1334477b5b29"; # 20.09-alpha
      ref = "release-20.09";
    }) { };
    USER = "main";

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
    '';

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
