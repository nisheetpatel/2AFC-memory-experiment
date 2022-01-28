# Experiment to test Human Memory
Two alternative forced-choice (2AFC) experiment.

## Installation
### Clone the git repository
`git clone https://github.com/nisheetpatel/Expt-HumanMemory` # clone repository

`cd Expt-HumanMemory` # change current directory to Expt-HumanMemory

### Check python and pip versions
Check your python version with `python --version` or `python3 --version`. The instructions below have been tested for python versions 3.6, 3.7, and 3.8. Also make sure that your pip is linked to your python 3.x with `pip --version` or `pip3 --version`.

Normally, you should be able to use `pip install -r requirements.txt`, but the wheels for psychopy and wxPython are not universal. Hence, most likely, this won't work in your case. Below, I have installation instructions for each OS separately.

### Install virtual envirionment
Note: use `pip3` instead of `pip` if that is what is linked to your python3.x 

`pip install virtualenv` # if not already installed

`virtualenv venv` # create virtual env folder in repo

`source venv/bin/activate` # activate it

### Linux
`pip install psychopy --user`

Then fetch a wxPython wheel for your platform from [here](https://extras.wxpython.org/wxPython4/extras/linux/gtk3/). After downloading the right wheel, you can then install it with something like:
`pip install path/to/your/wxpython.whl`

#### Installing psychtoolbox bindings
`sudo apt-get install libusb-1.0-0-dev portaudio19-dev libasound2-dev`

`pip install psychtoolbox`

### Mac OS
`pip install psychopy --user` # install psychopy

#### Installing psychtoolbox bindings
`sudo apt-get install libusb-1.0-0-dev portaudio19-dev libasound2-dev`

`pip install psychtoolbox`

### Windows
??

**Note**: If you still have issues with installation, please refer to the [official installation webpage](https://www.psychopy.org/download.html) for psychopy or contact me directly.

## Usage
`python main.py` will open up a window and gui with the experiment. Select options on each trial with left or right arrow keys. Hit 'escape' when options appear to exit the window.
