# `ae port-forward`
The `port-forward` command is used to forward network traffic on a local port to a port on a remote EC2 instance or ECS task container using Systems Manager Session Manager.

## Usage
- Forward `<port>` from localhost to `<port>` on the resource
  - `ae port-forward <resource> <port>`
- Forward `<local port>` from localhost to `<remote port>` on the resource
  - `ae port-forward <resource> <local port>:<remote port>`

### Aliases
- `ae pf`

### Options
None
