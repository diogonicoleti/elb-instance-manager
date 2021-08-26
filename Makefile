VERSION := $(shell cat VERSION)
DOCKER_IMAGE := $(shell jq -r .docker_image config.json)
PYTHON := python
TERRAFORM := terraform -chdir=deployments
TERRAFORM_PARAM := -var-file=../config.json -var="docker_tag=$(VERSION)"


.PHONY: setup clean build-image plan deploy-infra release deploy bump-version-patch bump-version-minor bump-version test run

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
	$(TERRAFORM) plan $(TERRAFORM_PARAM)

deploy-infra:
	$(TERRAFORM) apply $(TERRAFORM_PARAM)

release: build-image
	docker push $(DOCKER_IMAGE):$(VERSION)
	docker push $(DOCKER_IMAGE):latest

deploy: release deploy-infra

bump-version-patch:
	bumpversion --allow-dirty --current-version $(VERSION) patch VERSION

bump-version-minor:
	bumpversion --allow-dirty --current-version $(VERSION) minor VERSION

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) elb_instance_manager/app.py

.DEFAULT_GOAL := run
