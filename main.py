from pathlib import Path
from psychopy import visual, data
from expt.routines import TrialRoutine
from expt.conditions import TrialSequenceGenerator
from expt.options import createAllOptions
from expt.info import define_dialog_config_window, get_info_from_config_window

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

    # trial conditions
    trial_conditions = TrialSequenceGenerator(
        session_type=experiment_info["Session type"]
    ).generate()

    # trial and experiment data handlers
    trials = data.TrialHandler(trialList=trial_conditions, nReps=1, method="sequential")
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
