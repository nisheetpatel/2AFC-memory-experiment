from expt.option import createAllOptionSets
from pathlib import Path
from psychopy import visual, event, core, data, gui
import random

info = {}

# present dialog to collect info
info['Subject ID'] = ''
dlg = gui.DlgFromDict(info) #(and from psychopy import gui at top of script)
if not dlg.OK:
    core.quit()
#add additional info after the dialog has gone
info['fixTime'] = 0.5 # seconds
info['cueTime'] = 0.2
info['probeTime'] = 0.2
info['dateStr'] = data.getDateStr()

Path("./data").mkdir(parents=True, exist_ok=True)
fileName = f"data/{info['Subject ID']}"

win = visual.Window([1024,768], fullscr=False, units='pix')

# Initialize fixation cross
fixation = visual.ShapeStim(win=win, size=10, 
    vertices='cross', lineColor='white', fillColor='white')

# creating probe stimuli
optSets = createAllOptionSets(win=win)
allOptions = []
for optSet in optSets:
    allOptions.extend(optSet.options)

# initialize response clock
respClock = core.Clock()

# Example of conditions to be sent to TrialHandlerExt
conditions = [
    {"Name":0, "sA":1, "sB":2, "weight":4},
    {"Name":1, "sA":0, "sB":2, "weight":4},
    {"Name":2, "sA":0, "sB":1, "weight":4},
    {"Name":3, "sA":4, "sB":5, "weight":4},
    {"Name":4, "sA":3, "sB":5, "weight":4},
    {"Name":5, "sA":3, "sB":4, "weight":4},
    {"Name":6, "sA":7, "sB":8, "weight":1},
    {"Name":7, "sA":6, "sB":8, "weight":1},
    {"Name":8, "sA":6, "sB":7, "weight":1},
    {"Name":9, "sA":10, "sB":11, "weight":1},
    {"Name":10, "sA":9, "sB":11, "weight":1},
    {"Name":11, "sA":9, "sB":10, "weight":1}
]

# Trial handler
trials = data.TrialHandlerExt(trialList=conditions, 
    nReps=1, method='random')

# Experiment handler
thisExp = data.ExperimentHandler(
    name='humanMemory', version='0.0',
    extraInfo=info,
    dataFileName=fileName
)
thisExp.addLoop(trials)

# Run sequence of trials
for thisTrial in trials:
    # run one trial

    # assign left and right stimuli
    choiceOpts = [thisTrial["sA"], thisTrial["sB"]]
    random.shuffle(choiceOpts)

    # set position
    allOptions[choiceOpts[0]].setPosition(newPos=[-200,0])
    allOptions[choiceOpts[1]].setPosition(newPos=[200,0])

    s_left = allOptions[choiceOpts[0]].shape
    s_right = allOptions[choiceOpts[1]].shape

    # draw fixation and reset clock
    fixation.draw()
    win.flip()
    core.wait(1)

    # draw stimuli
    s_left.draw()
    s_right.draw()
    win.flip()
    respClock.reset()

    # wait for response
    keys = event.waitKeys(keyList = ['left', 'right', 'escape'])
    rt   = respClock.getTime()
    resp = keys[0]
    win.flip()

    if resp in ['left', 'right']:
        corr = 1
    elif resp=='escape':
        trials.finished = True
    
    # Inter-trial interval
    core.wait(1)

    # recording data
    trials.addData('resp', resp)
    trials.addData('rt', rt)
    thisExp.nextEntry()