# Welcome to the Adaptive Ground Point Filtering Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ssciwr/adaptivefiltering/CI)](https://github.com/ssciwr/adaptivefiltering/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/ssciwr/adaptivefiltering/branch/main/graph/badge.svg?token=ONIG38R74Y)](https://codecov.io/gh/ssciwr/adaptivefiltering)
[![Documentation Status](https://readthedocs.org/projects/adaptivefiltering/badge/)](https://adaptivefiltering.readthedocs.io/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ssciwr/adaptivefiltering/main)

**This library is currently under development.**

## Features

`adaptivefiltering` is a Python package to enhance the productivity of ground point filtering workflows in archaeology and beyond.
It provides a Jupyter-based environment for "human-in-the-loop" tuned, spatially heterogeneous ground point filterings.
Core features

* Working with Lidar datasets directly in Jupyter notebooks
  * Loading/Storing of LAS/LAZ files
  * Visualization using hillshade models and slope maps
  * Applying of ground point filtering algorithms
  * Cropping with a map-based user interface
* Accessibility of existing filtering algorithms under a unified data model:
  * [PDAL](https://pdal.io/): The Point Data Abstraction Library is an open source library for point cloud processing.
  * [OPALS](https://opals.geo.tuwien.ac.at/html/stable/index.html) is a proprietary library for processing Lidar data. It can be tested freely for datasets <1M points.
  * [LASTools](https://rapidlasso.com/) has a proprietary tool called `lasground_new` that can be used for ground point filtering.
* Access to predefined filter pipeline settings
  * Crowd-sourced library of filter pipelines at https://github.com/ssciwr/adaptivefiltering-library/
  * Filter definitions can be shared with colleagues as files
* Spatially heterogeneous application of filter pipelines
  * Assignment of filter pipeline settings to spatial subregions in map-based user interface
  * Command Line Interface for large scale application of filter pipelines

## Prerequisites

In order to work with `adaptivefiltering`, you need the following required pieces of Software.

* Python >= 3.7
* A [WebGL-enabled](https://get.webgl.org/) browser. We recommend Google Chrome and advise you to test with it whenever you experience difficulties with user intefaces.
* A [Conda installation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

There are alternatives to Conda for installation, but we strongly advise you to use Conda as it offers the best experience for this type of project.

## Installing and using

### Using Conda

Having a [local installation of Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), the following sequence of commands sets up a Conda environment for `adaptivefiltering`:

```
git clone https://github.com/ssciwr/adaptivefiltering.git
cd adaptivefiltering
conda env create -f environment.yml --force
conda run -n adaptivefiltering python -m pip install .
```

You can start the JupyterLab frontend by doing:

```
conda activate adaptivefiltering
jupyter lab
```

### Using Binder

You can try `adaptivefiltering` without prior installation by using [Binder](https://mybinder.org/v2/gh/ssciwr/adaptivefiltering/main), which is a free cloud-hosted service to run Jupyter notebooks. This will give you an impression of the library's capabilities, but you will want to work on a local setup when using the library productively: On Binder, you might experience very long startup times, slow user experience and limitations to disk space and memory.

### Using Docker

Having set up [Docker](https://docs.docker.com/get-docker/), you can use `adaptivefiltering` directly from a provided Docker image:

```
docker run -t -p 8888:8888 ssciwr/adaptivefiltering:latest
```

Having executed above command, paste the URL given on the command line into your browser and start using `adaptivefiltering` by looking at the provided Jupyter notebooks.
This image is limited to working with non-proprietary filtering backends (PDAL only).

### Using Pip

We advise you to use Conda as `adaptivefiltering` depends on a lot of other Python packages, some of which have external C/C++ dependencies. Using Conda, you get all of these installed automatically, using pip you might need to do a lot of manual work to get the same result.

That being said, `adaptivefiltering` can be installed from PyPI:

```
python -m pip install adaptivefiltering
```
