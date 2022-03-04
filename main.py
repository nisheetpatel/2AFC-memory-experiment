from psychopy import visual, data
from expt.options import SubjectSpecificOptions
from expt.routines import InitialScreen, TrialRoutine
from expt.conditions import TrialSequence
from expt.info import (
    display_config_window,
    get_config_info,
    load_subject_delta_pmt,
    save_subject_delta_pmt,
    set_file_path,
)

if __name__ == "__main__":
    # initialize info to begin session
    dialog_window = display_config_window()
    experiment_info = get_config_info(dialog_window)
    file_path = set_file_path(experiment_info)

    # create window for experiment
    win = visual.Window([1920, 1080], fullscr=True, units="pix", color=(-1, -1, -1))

    # create all stimuli
    choice_options = SubjectSpecificOptions(win=win)

    # initialize trial conditions and routine
    trial_conditions = TrialSequence(
        session_type=experiment_info["Session type"],
        session_id=experiment_info["Session ID"],
    ).generate()
    trial_routine = TrialRoutine(win=win, all_choice_options=choice_options.all_options)
    initial_screen = InitialScreen(win=win)

    # trial and experiment data handlers
    trials = data.TrialHandler(trialList=trial_conditions, nReps=1, method="sequential")
    this_exp = data.ExperimentHandler(extraInfo=experiment_info, dataFileName=file_path)
    this_exp.addLoop(trials)

    # initial screen
    initial_screen.show()

    # Run sequence of trials
    for this_trial in trials:
        # run one trial
        trial_routine.set_condition(condition=this_trial)
        trial_data = trial_routine.run()

        # record data
        for data_key, data_value in trial_data.items():
            trials.addData(data_key, data_value)

        # adaptive testing: set experimental parameter Delta_PMT adaptively
        # for each subject based on their performance in the test session 0
        if experiment_info["Session type"] == "testing":
            if int(experiment_info["Session ID"]) == 0:
                if trial_data["bonus_trial"]:
                    delta_pmt = choice_options.adapt_delta(
                        correct=trial_data["correct"]
                    )

                if trials.nRemaining == 0:
                    save_subject_delta_pmt(delta_pmt, experiment_info["Subject ID"])

            else:
                if trials.thisIndex == 0:
                    delta_pmt = load_subject_delta_pmt(experiment_info["Subject ID"])
                    choice_options.update_bonus_options(new_delta_pmt=delta_pmt)

        # indicate end of trial to experiment handler
        this_exp.nextEntry()
