PYTHON := python
TERRAFORM := terraform -chdir=deployments
DOCKER_IMAGE := dnicoleti/elb-instance-manager
VERSION := $(shell cat VERSION)


.PHONY: setup clean build-image plan deploy-infra release deploy test run bump-version-patch bump-version-minor bump-version

setup: requirements.txt
	pip install -r requirements.txt
	pip install bumpversion
	$(TERRAFORM) init

clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.egg-info' -exec rm -rf {} +

build-image:
	docker build -t $(DOCKER_IMAGE):$(VERSION) -t $(DOCKER_IMAGE):latest .

plan:
	$(TERRAFORM) plan

deploy-infra:
	$(TERRAFORM) apply

release: build-image
	docker push $(DOCKER_IMAGE):$(VERSION)
	docker push $(DOCKER_IMAGE):latest

deploy: release deploy-infra

bump-version-patch:
	bumpversion --allow-dirty --current-version $(VERSION) patch VERSION

bump-version-minor:
	bumpversion --allow-dirty --current-version $(VERSION) minor VERSION

bump-version: bump-version-minor

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) elb_instance_manager/app.py

.DEFAULT_GOAL := run
