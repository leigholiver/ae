# `ae logs`
The `logs` command is used to view or follow one or more Cloudwatch Log Groups.

## Usage
- `ae logs [-f|--follow] [-s|--since <seconds>] <resource> [<resource> ...]`

### Aliases
- `ae l`

### Options
#### `-f`/`--follow`
Continually check for and append new log lines

#### `-s`/`--since`
Time in minutes to look back for initial log messages.
Default is 5 minutes.
