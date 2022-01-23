from pathlib import Path
import pdb
from psychopy import visual, core, data, gui
from expt.routines import TrialRoutine
from expt.options import createAllOptions
from expt.conditions import training_trial_conditions

def define_dialog_config_window() -> gui.Dlg:
    dialog = gui.Dlg(title="Memory Experiment 1")
    dialog.addField('Subject ID')
    dialog.addText('Session Settings')
    dialog.addField('Session ID')
    dialog.addField('Session Type', choices=['practice','training','testing'])

    ok_data = dialog.show()  # show dialog and wait for OK or Cancel
    if dialog.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print('user cancelled')

    return dialog


def get_info_from_config_window(dialog_window):
    # add date to info
    info["dateStr"] = data.getDateStr()



if __name__=='__main__':
    # initialize info to begin session
    dialog_window = define_dialog_config_window()
    from pdb import set_trace; set_trace()
  

    # ensure data path exists
    Path("./data").mkdir(parents=True, exist_ok=True)

    # # get info from config window
    # # set file name to save data
    # subj = f"subj_{info['Subject ID']}"
    # sess = f"_sess_{info['Session ID']}"
    # sType = f"_type_{info['Session Type']}"
    # sDate = f"_{info['dateStr']}"
    # fileName = f"data/" + subj + sess + sType + sDate

    # # creating the experiment
    # # create window
    # win = visual.Window([1024, 768], fullscr=False, units="pix")

    # # create probe stimuli
    # allOptions = createAllOptions(win=win)

    # # trial and experiment data handlers
    # trials = data.TrialHandlerExt(trialList=training_trial_conditions, nReps=1, method="random")
    # thisExp = data.ExperimentHandler(
    #     name="humanMemory", version="0.1", extraInfo=info, dataFileName=fileName
    # )
    # thisExp.addLoop(trials)

    # # Run sequence of trials
    # for thisTrial in trials:
    #     # run one trial
    #     trialRoutine = TrialRoutine(condition=thisTrial, win=win, allOptions=allOptions)
    #     rt, resp, corr, rew = trialRoutine.run()

    #     # close if user hit escape
    #     if resp == "escape":
    #         trials.finished = True

    #     # recording data
    #     trials.addData("response", resp)
    #     trials.addData("rt", rt)
    #     trials.addData("correct", corr)
    #     trials.addData("rewardObtained", rew)
    #     thisExp.nextEntry()