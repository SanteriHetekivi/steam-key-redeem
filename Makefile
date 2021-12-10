.PHONY: install_pacman install_requirements
.DEFAULT_GOAL := install_requirements

# Install packages with pacman.
install_pacman:
	sudo pacman -S python python-pip

# Install requirements with pip.
install_requirements:
	pip install -r requirements.txt
