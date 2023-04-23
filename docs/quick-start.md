# Getting Started

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
