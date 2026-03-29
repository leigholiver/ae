{
  description = "ae";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
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
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
          mkPoetryApplication
          mkPoetryEnv
          defaultPoetryOverrides
          ;
        overrides = defaultPoetryOverrides.extend (
          final: prev: {
            pyproject-hooks = pkgs.python3Packages.pyproject-hooks;
            build = pkgs.python3Packages.build;
            pyyaml = pkgs.python3Packages.pyyaml;
            boto3 = pkgs.python3Packages.boto3;
            click = pkgs.python3Packages.click;
            click-aliases = pkgs.python3Packages.click-aliases;
            colorama = pkgs.python3Packages.colorama;
            inquirerpy = pkgs.python3Packages.inquirerpy;
            requests-aws4auth = pkgs.python3Packages.requests-aws4auth;
          }
        );
      in
      {
        formatter = nixpkgs.legacyPackages.${system}.nixfmt;

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
