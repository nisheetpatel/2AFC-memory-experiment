from pathlib import Path
from psychopy import visual, core, data, gui
from expt.routines import TrialRoutine
from expt.options import createAllOptions
from expt.conditions import training_trial_conditions


def define_dialog_config_window() -> gui.Dlg:
    dialog = gui.Dlg(title="Memory Experiment")
    dialog.addText("Subject Settings")
    dialog.addField("Subject ID")
    dialog.addText("Session Settings")
    dialog.addField("Session ID")
    dialog.addField("Session Type", choices=["practice", "training", "testing"])
    dialog.addField(
        "Instruction set", choices=["first session", "this ain't yo mama's first rodeo"]
    )

    ok_data = dialog.show()  # show dialog and wait for OK or Cancel
    if dialog.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print("\nUser cancelled!\n")
        core.quit()

    return dialog


def get_info_from_config_window(dialog_window):
    experiment_info = {
        "Subject ID": dialog_window.data[0],
        "Session ID": dialog_window.data[1],
        "Session type": dialog_window.data[2],
    }

    # add date to info
    experiment_info["dateStr"] = data.getDateStr()

    return experiment_info


if __name__ == "__main__":
    # initialize info to begin session
    dialog_window = define_dialog_config_window()
    experiment_info = get_info_from_config_window(dialog_window)

    # ensure data path exists and define file name to save data to
    Path("./data").mkdir(parents=True, exist_ok=True)
    fileName = "data/subj_{}_sess_{}_{}_{}".format(*experiment_info.values())

    # creating the experiment
    # create window
    win = visual.Window([1024, 768], fullscr=False, units="pix")

    # create probe stimuli
    allOptions = createAllOptions(win=win)

    # trial and experiment data handlers
    trials = data.TrialHandlerExt(
        trialList=training_trial_conditions, nReps=1, method="random"
    )
    thisExp = data.ExperimentHandler(
        name="humanMemory",
        version="0.1",
        extraInfo=experiment_info,
        dataFileName=fileName,
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
