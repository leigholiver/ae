.PHONY: shell build update

default: shell

shell:
	nix develop .

build:
	nix build .#

update:
	nix flake update
