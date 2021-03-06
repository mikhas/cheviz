# Cheviz
> Showcase Data engineering and ETL pipelines with chess.


## 1. Project goals

### 1.0 Learn stuff.

### 1.1 Start a project with publishable documentation from the beginning.

Usually you'd hack on your code, then at one point think you can push it out to github and make a series of blog post to talk about the cool stuff you did. I think that's deeply flawed and too cumbersome. So let's try to start with documentation first, then start implementing your ideas from top to bottom, talking about them while you are trying to get them to work. Hopefully that makes the documentation less hand-wavy and less likely to gloss over details.

### 1.2 Have a proper ETL pipeline, from data to insights.

One goal is to make chess visible in a way that we can approach it like any other data. If we embed the effect of pieces on the board differently, we can reduce a chess game to a series of 8x8 matrices over $\mathbb{N}$. See figure below.
![Visualized metrics from 1953 candidates tournament](images/euwe-najdorf-zurich1953.png "Visualized metrics from 1953 candidates tournament")

## 2. Install

### 2.1 miniconda

You might want to start from miniconda, especially if you are on Windows or an older Linux distribution.
See https://docs.conda.io/en/latest/miniconda.html for installing miniconda.

The `requirements.txt` exists to help setup your conda environment. To install all dependencies into your new conda environment, including pytorch and fastai, use the following command:

`$ conda create --name [ENV] --channel pytorch --channel fastai --file requirements.txt`

## 3. Hacking

### 3.1 nbdev

Install nbdev via `pip install nbdev`. Before doing anything else, install the nbdev git hooks via `nbdev_install_git_hooks` otherwise git and Jupyter won't play well together. See https://nbdev.fast.ai/ for details.

You can run `make` to update the Python library `cheviz` from the Jupyter notebooks. This also updates the `README.md`. Remember to adjust `settings.ini` as needed.

### 3.2 Jupyter widgets

For JupyterLab, just installing ipywidgets via conda isn't enough. We also need nodejs (sigh) because JupyterLab has an extensions system now. Apparently it causes some frustration among users because it wasn't clearly communicated why upgrading from Jupyter Notebooks to JupyterLab broke important functionality. Anyway, we install ipywidgets like so:

```bash
$ conda install -n [ENV] -c conda-forge ipywidgets
$ conda install -n [ENV] -c conda-forge nodejs
$ conda activate [ENV]
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

This requires a restart of the Jupyter server to take effect.
