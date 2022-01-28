# Experiment to test Human Memory
Two alternative forced-choice (2AFC) experiment.

## Installation
#### Clone the git repository
`git clone https://github.com/nisheetpatel/Expt-HumanMemory` # clone repository

`cd Expt-HumanMemory` # change current directory to Expt-HumanMemory

#### Check python and pip versions
Check that your python version with `python --version` or `python3 --version`. The instructions below have been tested for python versions 3.6, 3.7, and 3.8. Also make sure that your pip is linked to your python 3.x with `pip --version` or `pip3 --version`.

Normally, you should be able to use `pip install -r requirements.txt`, but the wheels for psychopy and wxPython are not universal. Hence, most likely, this won't work in your case. Below, I have installation instructions for each OS separately.

#### Install virtual envirionment
Note: use `pip3` instead of `pip` if that is what is linked to your python3.x 

`pip install virtualenv` # if not already installed

`virtualenv venv` # create virtual env folder in repo

`source venv/bin/activate` # activate it

#### Linux (Ubuntu 20.04)
`pip install psychopy`

#### Mac OS
`pip install psychopy` # install psychopy

#### Windows
??

## Usage
`python main.py` will open up a window and gui with the experiment. Select options on each trial with left or right arrow keys. Hit 'escape' when options appear to exit the window.
