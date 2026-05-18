{
  description = "ae";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
    };
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      poetry2nix,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        p2nPkgs = poetry2nix.inputs.nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = p2nPkgs; })
          mkPoetryApplication
          mkPoetryEnv
          defaultPoetryOverrides
          ;
        overrides = defaultPoetryOverrides.extend (
          final: prev: {
            pyproject-hooks = p2nPkgs.python3Packages.pyproject-hooks;
            build = p2nPkgs.python3Packages.build;
            pyyaml = p2nPkgs.python3Packages.pyyaml;
            boto3 = p2nPkgs.python3Packages.boto3;
            click = p2nPkgs.python3Packages.click;
            click-aliases = p2nPkgs.python3Packages.click-aliases;
            colorama = p2nPkgs.python3Packages.colorama;
            inquirerpy = p2nPkgs.python3Packages.inquirerpy;
            requests-aws4auth = p2nPkgs.python3Packages.requests-aws4auth;
          }
        );
      in
      {
        formatter = pkgs.nixfmt;

        packages.default = mkPoetryApplication {
          projectDir = self;
          preferWheels = true;
          inherit overrides;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.poetry
            pkgs.python3Packages.bump2version
            (mkPoetryEnv {
              projectDir = self;
              preferWheels = true;
              inherit overrides;
            })
          ];
        };
      }
    );
}
