import numpy
import expt
from pathlib import Path
from psychopy import visual, event, core, data, gui

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

# create probe stimuli
# Initialize fixation cross
s_left = visual.Circle(win=win, size=100, pos=[200,0],
    lineColor='green', fillColor='green', colorSpace='rgb')
s_right = visual.Pie(win=win, size=100, pos=[-200,0],
    start=60, end=-240, lineColor='red', fillColor='red',
    colorSpace='rgb')

# initialize response clock
respClock = core.Clock()

# Trial handler
trials = data.TrialHandler(trialList=[], nReps=5)

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

    # draw fixation and reset clock
    fixation.draw()
    win.flip()
    respClock.reset()
    core.wait(1)

    # draw stimuli
    s_left.draw()
    s_right.draw()
    win.flip()

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


# Example of conditions to be sent to TrialHandlerExt
# trialList = [
#     {"Name":0, "sA":1, "sB":2, "weight":2},
#     {"Name":1, "sA":0, "sB":2, "weight":1}
# ]