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

    # initialize trial conditions and routine
    trial_conditions = TrialSequence(experiment_info["Session type"]).generate()
    trial_routine = TrialRoutine(win=win, all_choice_options=choice_options)

    # trial and experiment data handlers
    trials = data.TrialHandler(trialList=trial_conditions, nReps=1, method="sequential")
    this_exp = data.ExperimentHandler(extraInfo=experiment_info, dataFileName=file_path)
    this_exp.addLoop(trials)

    # Run sequence of trials
    for this_trial in trials:
        # run one trial
        trial_routine.set_condition(condition=this_trial)
        data_keys, data_values = trial_routine.run()

        # record data
        for data_key, data_value in zip(data_keys, data_values):
            trials.addData(data_key, data_value)

        # indicate end of trial to experiment handler
        this_exp.nextEntry()
