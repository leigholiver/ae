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


## Docs
- [Installation and Getting Started](./quick-start)
- [Configuration Reference](./configuration)
- Command reference
  - [`ae connect`](./connect)
  - [`ae run-command`](./run-command)
  - [`ae port-forward`](./port-forward)
  - [`ae logs`](./logs)
- [Extending `ae`](./extending)
