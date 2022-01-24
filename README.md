# Experiment to test Human Memory
Two alternative forced-choice (2AFC) experiment.

## Installation
`git clone https://github.com/nisheetpatel/Expt-HumanMemory` # clone repository

`cd Expt-HumanMemory`

`pip install virtualenv` # if not already installed

`virtualenv venv` # create virtual env folder in repo

`source venv/bin/activate` # activate it

`pip install psychopy` # install psychopy

`pip install wxPython` # install wxPython

Note: You could try to install everything with `pip install -r requirements.txt`, however it fails because of a couple of issues. 
wxPython cannot be included in the requirements.txt because [this](https://github.com/psychopy/psychopy/issues/2418). If wxPython installation fails on Linux: see [this](https://wxpython.org/pages/downloads/index.html).


## Usage
`python main.py` will open up a window and gui with the experiment. Select options on each trial with left or right arrow keys. Hit 'escape' when options appear to exit the window.
