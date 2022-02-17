from pathlib import Path
from psychopy import visual, data
from expt.options import create_choice_options
from expt.routines import TrialRoutine
from expt.conditions import TrialSequence
from expt.info import display_config_window, get_config_info, set_file_path

if __name__ == "__main__":
    # initialize info to begin session
    dialog_window = display_config_window()
    experiment_info = get_config_info(dialog_window)
    file_path = set_file_path(experiment_info)

    # create window for experiment
    win = visual.Window([1024, 768], fullscr=False, units="pix")

    # create all stimuli
    choice_options = create_choice_options(win)

    # trial conditions
    trial_conditions = TrialSequence(
        session_type=experiment_info["Session type"]
    ).generate()

    # trial and experiment data handlers
    trials = data.TrialHandler(trialList=trial_conditions, nReps=1, method="sequential")
    this_exp = data.ExperimentHandler(extraInfo=experiment_info, dataFileName=file_path)
    this_exp.addLoop(trials)

    # Run sequence of trials
    for this_trial in trials:
        # run one trial
        trial_routine = TrialRoutine(
            condition=this_trial, win=win, choice_options=choice_options
        )
        data_keys, data_values = trial_routine.run()

        # record data
        for data_key, data_value in zip(data_keys, data_values):
            trials.addData(data_key, data_value)

        # indicate end of trial to experiment handler
        this_exp.nextEntry()
