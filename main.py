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

# # create probe stimuli
# s_left = visual.Circle(win=win, size=100, pos=[200,0],
#     lineColor='green', fillColor='green', colorSpace='rgb')
# s_right = visual.Pie(win=win, size=100, pos=[-200,0],
#     start=60, end=-240, lineColor='red', fillColor='red',
#     colorSpace='rgb')

# creating probe stimuli
# reds
s_hexagon = visual.Polygon(win, edges=6, size=100, pos=[200,0],
    lineColor='red', fillColor='red', colorSpace='rgb')

s_triangle = visual.Polygon(win, edges=3, size=100, pos=[-200,0],
    lineColor='red', fillColor='red', colorSpace='rgb')

s_rectangle = visual.Polygon(win, edges=4, size=[100,50], pos=[-200,0],
    lineColor='red', fillColor='red', colorSpace='rgb')

# blues
s_diamond = visual.Polygon(win, edges=4, size=100, pos=[200,0],
    ori=45, lineColor='blue', fillColor='blue', colorSpace='rgb')

s_oval = visual.Circle(win=win, radius=[50,25], pos=[-200,0],
    ori=45, lineColor='blue', fillColor='blue')

s_star = visual.ShapeStim(win=win, pos=[-200,0], vertices='star7',
    size=100, lineColor='blue', fillColor='blue')

# greens
s_cross = visual.ShapeStim(win, pos=[200,0], vertices='cross',
    size=100, ori=45, lineColor='green', fillColor='green')

s_pentagon = visual.Polygon(win, edges=5, size=100, pos=[-200,0],
    lineColor='green', fillColor='green', colorSpace='rgb')

s_circle = visual.Circle(win=win, size=100, pos=[-200,0],
    lineColor='green', fillColor='green', colorSpace='rgb')

# yellows
s_octagon = visual.Polygon(win, edges=8, size=100, pos=[200,0],
    lineColor='yellow', fillColor='yellow', colorSpace='rgb')

s_plus = visual.ShapeStim(win, pos=[-200,0], vertices='cross',
    size=100, lineColor='yellow', fillColor='yellow')

s_pacman = visual.Pie(win=win, size=100, pos=[-200,0],
    start=60, end=-240, lineColor='yellow', fillColor='yellow',
    colorSpace='rgb')

# collecting all stimuli in a list
stims = [s_hexagon, s_triangle, s_rectangle, 
        s_diamond, s_oval, s_star,
        s_cross, s_pentagon, s_circle,
        s_octagon, s_plus, s_pacman]

# initialize response clock
respClock = core.Clock()

# Example of conditions to be sent to TrialHandlerExt
trialList = [
    {"Name":0, "sA":0, "sB":1, "weight":2},
    {"Name":1, "sA":0, "sB":2, "weight":2},
    {"Name":2, "sA":3, "sB":4, "weight":2},
    {"Name":3, "sA":3, "sB":5, "weight":2},
    {"Name":4, "sA":6, "sB":7, "weight":1},
    {"Name":5, "sA":6, "sB":8, "weight":1},
    {"Name":6, "sA":9, "sB":10, "weight":1},
    {"Name":7, "sA":9, "sB":11, "weight":1}
]

# Trial handler
trials = data.TrialHandlerExt(trialList=trialList, 
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

    # draw fixation and reset clock
    fixation.draw()
    win.flip()
    respClock.reset()
    core.wait(1)

    # assign left and right stimuli
    s_left = stims[thisTrial["sA"]]
    s_right = stims[thisTrial["sB"]]

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