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
