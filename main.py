from pathlib import Path
from psychopy import visual, data
from expt.routines import TrialRoutine
from expt.conditions import TrialSequenceGenerator
from expt.info import display_config_window, get_config_info, set_file_path

if __name__ == "__main__":
    # initialize info to begin session
    dialog_window = display_config_window()
    experiment_info = get_config_info(dialog_window)
    file_path = set_file_path(experiment_info)

    # create window for experiment
    win = visual.Window([1024, 768], fullscr=False, units="pix")

    # trial conditions
    trial_conditions = TrialSequenceGenerator(
        session_type=experiment_info["Session type"]
    ).generate()

    # trial and experiment data handlers
    trials = data.TrialHandler(trialList=trial_conditions, nReps=1, method="sequential")
    this_exp = data.ExperimentHandler(extraInfo=experiment_info, dataFileName=file_path)
    this_exp.addLoop(trials)

    # Run sequence of trials
    ## INEFFICIENT IMPLEMENTATION!!!
    ## currently creates a new object for each trial
    ## also trial routine creates 12 new stimuli for each trial
    ## change this
    for this_trial in trials:
        # run one trial
        trial_routine = TrialRoutine(condition=this_trial, win=win)
        rt, resp, corr, rew = trial_routine.run()

        # close if user hit escape
        if resp == "escape":
            trials.finished = True

        # recording data
        trials.addData("response", resp)
        trials.addData("rt", rt)
        trials.addData("correct", corr)
        trials.addData("rewardObtained", rew)
        this_exp.nextEntry()
