###
# Clean
###


TARGET := oru2xds.egg-info build target

.PHONY: clean
clean:
	rm -rf $(TARGET)
	rm -rf dist/*

###
# Build
###

.PHONY: build
build:
	# Make sure you have required packages installed
	# sudo apt install python3-pip python3-setuptools python3-wheel python3-build
	# sudo apt install python3.11-venv twine
	rm -rf dist/*
	python3 -m build
	python3 -m twine upload dist/*
	# Shifting to the next release version
	echo "$$(awk -F. '{$$3=$$3+1;print;}' OFS=. ORS="\"\n" src/oru2xds/__version__.py)" > src/oru2xds/__version__.py


###
# Backup
###

BACKUP_VER=$(shell cat backups/backup_next_version)

.PHONY: backup
backup:
	@echo Next backup version is $(BACKUP_VER)
	tar -zcvf backups/oru2xds-$(BACKUP_VER).tgz src/oru2xds/*.py *.md tests Dockerfile Makefile pyproject.toml src/oru2xds/examples
	echo $(BACKUP_VER) + 1 | bc > backups/backup_next_version

	
###
# Docker
###

.PHONY: docker
docker:
	- docker image rm antocm/oru2xds
	docker build -t antocm/oru2xds .
	docker push antocm/oru2xds
	
###
# Run Docker image
###

.PHONY: rundocker
rundocker:
	docker run -it --rm -p 2575:2575 antocm/oru2xds

