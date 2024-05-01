# WQU Grader Workshop

This repository contains the materials for the WQU Grader Workshop. The workshop is designed to help you get started with grading assignments on the WQU platform.

# Installation

## Step 1: Install Linux Terminal

You will use the terminal to manage the grading server.

**Windows Users:** You can install the Windows Subsystem for Linux (WSL) by following the instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install).

**Mac and Linux Users:** You can use the terminal that comes with your operating system.

## Step 2: Install Python and Environment Manager

You will use Anaconda to build the environment that the grader server needs to run.

**Windows, Mac, and Linux Users:** You can install Anaconda by following the instructions [here](https://docs.anaconda.com/free/anaconda/install/index.html).

## Step 3: Install Docker Desktop

You will use Docker to run a version of the virtual machine that students  use to complete their assignments.

**Windows, Mac, and Linux Users:** You can install Docker Desktop by following the instructions [here](https://www.docker.com/products/docker-desktop/).

## Step 4: Build the Grader Environment

You will use your terminal and Anaconda to build the grader environment.

- Open your terminal or WSL. 
- Check that Anaconda is installed by running `conda --version`.
- Create a new environment by running `conda create --name grader python=3.11`. When asked if you want to proceed, type `y` and press `Enter`.
- Activate the environment by running `conda activate grader`.
- Install the `grading-tools` library and Jupyter Lab by running `pip install grading-tools jupyterlab`.