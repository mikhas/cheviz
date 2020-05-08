# Cheviz
> An example project to analyze chess positions via visual metrics.


# 1. Project goals

### 1.0 Learn stuff.

### 1.1 Start a project with publishable documentation from the beginning.

Usually you'd hack on your code, then at one point think you can push it out to github and make a series of blog post to talk about the cool stuff you did. I think that's deeply flawed and too cumbersome. So let's try to start with documentation first, then start implementing your ideas from top to bottom, talking about them while you are trying to get them to work. Hopefully that makes the documentation less hand-wavy and less likely to gloss over details.

### 1.2 Have a proper ETL pipeline, from data to insights.

# 2. Install

## 2.1 miniconda

You might want to start from miniconda, especially if you are on Windows or an older Linux distribution.
See https://docs.conda.io/en/latest/miniconda.html for installing miniconda.

The `requirements.txt` exists to help setup your conda environment. To install all dependencies into your new conda environment, including pytorch and fastai, use the following command:

`$ conda create --name [ENV] --channel pytorch --channel fastai --file requirements.txt`

# 3. Hacking

Install nbdev via `pip install nbdev`. Before doing anything else, install the nbdev git hooks via `nbdev_install_git_hooks` otherwise git and Jupyter won't play well together. See https://nbdev.fast.ai/ for details.

You can run `make` to update the Python library `cheviz` from the Jupyter notebooks. This also updates the `README.md`. Remember to adjust `settings.ini` as needed.
