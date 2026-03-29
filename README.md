# ae
`ae` ("awscli extended") is a CLI tool aiming to simplify various AWS tasks, taking inspiration from `kubectl`, `docker`, `docker-compose` etc.

Features:
- Fast and consistent interface for:
  - Connecting and getting an interactive shell on instances/containers
  - Running commands on multiple instances/containers
  - Forwarding ports to instances/containers
- Viewing logs from one or more Cloudwatch log groups
- Easily using multiple AWS accounts and assumed IAM roles
- Extendible by adding custom subcommands from local files or pip packages

## Installation
Requirements:
- Python and pip
- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- AWS CLI [Session manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

Install or upgrade using pip:
- `pip install --upgrade git+ssh://git@github.com/leigholiver/ae.git`

## Quick start
```bash
$ ae [-p/--profile <aws cli profile>] <command> [--help]
```

- Connect to an EC2 instance or ECS task container
    - `ae connect <name>`
- Run a command on an instance/container
    - `ae run-command <name> -- command`
- Forward a local port to an instance/container
    - `ae port-forward <name> <local port>:<remote port>`
- View CloudWatch logs from one or more log groups
    - `ae logs [-f] <name> [<name>...]`
- Select an AWS CLI profile to use
    - `ae -p <aws cli profile> <command>`

> Full usage instructions can be found in the [documentation](https://leigholiver.com/ae)

### Nix
Add this repo to your flake inputs
```nix
inputs = {
  ae.url = "github:leigholiver/ae";
};
```

If you have `nixpkgs` or `poetry2nix` in your flake inputs, you can pin ae's dependencies to your versions:
```nix
inputs = {
  ae = {
    url = "github:leigholiver/ae";
    inputs.nixpkgs.follows = "nixpkgs";
    inputs.poetry2nix.follows = "poetry2nix";
  };
};
```

Install the package
```nix
# nixos
environment.systemPackages = [ inputs.ae.packages.${pkgs.system}.default ];
# home-manager
home.packages = [ inputs.ae.packages.${pkgs.system}.default ];
```

#### dev/build
The flake provides a dev shell which can be entered with `nix develop`.
In the dev shell, running `ae` will use the local dev version.

To build the package, run `nix build`, and the output will be placed in the `result/` directory.
