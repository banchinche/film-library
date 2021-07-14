# import dev config.
# You can change the default config with `make cnf="config_special.env" build`
dev-cnf ?= .env.dev
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

# import prod config
# You can change the default deploy config with `make cnf="deploy_special.env" release`
prod-cnf ?= .env.prod
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))


# import prod db config
# You can change the default deploy config with `make cnf="deploy_special.env" release`
dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


#DOCKER TASKS

up: docker-compose up

stop: docker-compose stop

down: docker-compose down