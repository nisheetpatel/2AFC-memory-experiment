# Experiment to test Human Memory
Two alternative forced-choice (2AFC) experiment.

## Installation
- Clone current repository
`git clone https://github.com/nisheetpatel/Expt-HumanMemory`

- Change directory
`cd Expt-HumanMemory`

- If not already installed, install virtualenv
`pip install virtualenv`

- Create a new env folder into the project folder
`virtualenv venv`

- Activate the virtual envrionment
`source venv/bin/activate`

- Install required packages
`pip install -r requirements.txt`

- Install wxPython
  - cannot be included in the requirements.txt because [this](https://github.com/psychopy/psychopy/issues/2418)
  - it may fail on Linux: see [this](https://wxpython.org/pages/downloads/index.html)
`pip install wxPython`

## Usage
`python main.py` will open up a window and gui with the experiment. Select options on each trial with left or right arrow keys. Hit 'escape' when options appear to exit the window.
