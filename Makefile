# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

DOCKER_COMPOSE_OPTS=--env-file .env -f docker-compose.yml

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start: ## Spin up the project
	docker-compose $(DOCKER_COMPOSE_OPTS) up -d

build: ## Build up the project
	docker-compose $(DOCKER_COMPOSE_OPTS) up -d  --build

ps: ## List project containers
	docker-compose $(DOCKER_COMPOSE_OPTS) ps

stop: ## Stop the project
	docker-compose $(DOCKER_COMPOSE_OPTS) stop

destroy: ## Remove all the docker compose artifacts
	docker-compose $(DOCKER_COMPOSE_OPTS) stop
	docker-compose $(DOCKER_COMPOSE_OPTS) rm -f

connect: ## connect to the container
	docker-compose $(DOCKER_COMPOSE_OPTS) exec oidc-front bash

logs: ## show logs of the container
	docker-compose $(DOCKER_COMPOSE_OPTS) logs oidc-front

install-helmfile: ## install all helm charts from helmfile
	helmfile --state-values-set user=user33  apply --set user=user33
	helmfile --state-values-set user=user1337  apply --set user=user1337

uninstall-helmfile: ## uninstall all helm charts from helmfile
	helmfile --state-values-set user=user33  destroy
	helmfile --state-values-set user=user1337  destroy

install-okta-protected-endpoint: ## install helm chart firewalled-test
	helm upgrade -n okta-protected-endpoint --create-namespace --install okta-protected-endpoint releases/okta-protected-endpoint

install-okta-firewall: ## install helm chart okta-sp-test
	helm upgrade -n okta-firewall --create-namespace --install okta-firewall releases/okta-firewall

uninstall-okta-protected-endpoint: ## uninstall helm chart firewalled-test
	helm uninstall -n okta-protected-endpoint okta-protected-endpoint

uninstall-okta-firewall: ## uninstall helm chart okta-sp-test
	helm uninstall -n okta-firewall okta-firewall

push-to-registry: ## manually push container, testing purpose
	docker tag oidc-test_oidc-front:latest kwop/oidctest:latest
	docker push kwop/oidctest:latest

boum: ## destroy / remove all containers on the machine
	for f in $$(docker ps -a -q); do docker stop $$f; done
	docker system prune --volumes -f
