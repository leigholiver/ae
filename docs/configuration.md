# Configuring `ae`
`ae` will attempt to read your AWS accounts and roles from the AWS CLI configuration.
You can choose a specific AWS profile using `ae -p/--profile <profile> <command>`.

`ae` can be configured using settings in the configuration file at either:
- `~/.ae/ae.yml`
- `~/.ae/<profile>.yml` if an AWS CLI profile has been specified.

## Configuration Reference
### `aws-profile`
The name of an AWS CLI profile to use.
This can be used to override the chosen profile, or be set to `null` to force `ae` to use credentials from environment variables.
This can be useful when used in conjunction with `aws-vault`.

### `aws-region`
The AWS region to use, overriding the AWS CLI config

### `role-source-profile`
An AWS CLI profile to read assume role configuration from, if different to `aws-profile`.
This can be useful when used in conjunction with `aws-vault`.

### `roles`
A list of IAM role names to retrieve from the specified profile.
If unset, `ae` will read all roles from the profile.

### `ignore-roles`
A list of IAM role names to ignore from the specified profile.
By default `ae` will read all roles from the profile.

### `cache-time`
The number of seconds to cache resources for.
This can be set to `0` to refresh the resources on every execution.

### `cache-credentials`
Whether to keep a local cache of temporary credentials.
By default, `ae` will keep a cache of temporary credentials to speed up execution.
Set this to `false` to disable this behaviour.

### `session`
- `name`: The name to use for Systems Manager and IAM sessions
- `duration`: The length of IAM sessions in seconds
