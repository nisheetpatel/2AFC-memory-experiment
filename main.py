from pathlib import Path
from psychopy import visual, core, data, gui
from expt.routines import TrialRoutine
from expt.options import createAllOptions
from expt.conditions import trialConditions

# initialize info to begin session
info = {"Subject ID": "", "Session ID": "", "Session Type": ""}

# present GUI to collect info
dlg = gui.DlgFromDict(info)

if not dlg.OK:
    core.quit()

# add date to info
info["dateStr"] = data.getDateStr()

# ensure data path exists
Path("./data").mkdir(parents=True, exist_ok=True)

# set file name to save data
subj = f"subj_{info['Subject ID']}"
sess = f"_sess_{info['Session ID']}"
sType = f"_type_{info['Session Type']}"
sDate = f"_{info['dateStr']}"
fileName = f"data/" + subj + sess + sType + sDate

# create window
win = visual.Window([1024, 768], fullscr=False, units="pix")

# create probe stimuli
allOptions = createAllOptions(win=win)

# trial and experiment data handlers
trials = data.TrialHandlerExt(trialList=trialConditions, nReps=1, method="random")
thisExp = data.ExperimentHandler(
    name="humanMemory", version="0.1", extraInfo=info, dataFileName=fileName
)
thisExp.addLoop(trials)

# Run sequence of trials
for thisTrial in trials:
    # run one trial
    trialRoutine = TrialRoutine(condition=thisTrial, win=win, allOptions=allOptions)
    rt, resp, corr, rew = trialRoutine.run()

    # close if user hit escape
    if resp == "escape":
        trials.finished = True

    # recording data
    trials.addData("response", resp)
    trials.addData("rt", rt)
    trials.addData("correct", corr)
    trials.addData("rewardObtained", rew)
    thisExp.nextEntry()
