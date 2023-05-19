.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

install_over:
	go get github.com/opa-oz/over@latest

over_major:
	over up --major --inplace --verbose

over_minor:
	over up --minor --inplace --verbose

over_patch:
	over up --patch --inplace --verbose