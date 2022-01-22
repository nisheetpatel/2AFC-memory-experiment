from expt.options import createAllOptionSets, feedbackRect, feedbackText, fixCross
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
info['fixTime'] = 1 # seconds
info['probeTime'] = 5
info['dateStr'] = data.getDateStr()

Path("./data").mkdir(parents=True, exist_ok=True)
fileName = f"data/{info['Subject ID']}"

win = visual.Window([1024,768], fullscr=False, units='pix')

# Initialize fixation cross
fixation = fixCross(win=win)
feedbackSq = feedbackRect(win=win)

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
    allOptions[choiceOpts[0]].setPosition(newPos='left')
    allOptions[choiceOpts[1]].setPosition(newPos='right')

    s_left = allOptions[choiceOpts[0]]
    s_right = allOptions[choiceOpts[1]]

    # draw fixation and reset clock
    fixation.shape.draw()
    win.flip()
    core.wait(1)

    # draw stimuli
    s_left.shape.draw()
    s_right.shape.draw()
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

    # feedback
    s_left.shape.draw()
    s_right.shape.draw()
    feedbackSq.setPosition(resp)
    feedbackSq.shape.draw()
    if resp == 'left':
        r = s_left.generateReward()
    elif resp == 'right':
        r = s_right.generateReward()
    feedbackTxt = feedbackText(win, rewardObtained=r)
    feedbackTxt.setPosition(resp)
    feedbackTxt.shape.draw()
    win.flip()
    
    # Inter-trial interval
    core.wait(1)

    # recording data
    trials.addData('resp', resp)
    trials.addData('rt', rt)
    thisExp.nextEntry()