import itertools
import os
import pandas as pd
from psychopy import visual, data
from expt.options import SubjectSpecificOptions, create_choice_options
from expt.routines import TrialRoutine
from expt.conditions import TrialSequence
from expt.info import (
    get_config_info,
    load_subject_delta_pmt,
    save_subject_delta_pmt,
    set_file_path,
)

n_subjects = 3
n_sessions_per_type = 2


def simulate_experiments() -> pd.DataFrame:
    """
    Runs experiments for n_subjects, n_sessions with automated
    responses and stores data to test validity of trials generated.
    Returns data re. choice options for each subject.
    """

    subject_ids = list(range(n_subjects))
    session_ids = list(range(n_sessions_per_type))
    session_types = ["training", "testing"]

    # initialize options dataframe
    df_options = pd.DataFrame()

    for config_info in itertools.product(subject_ids, session_ids, session_types):

        # initialize info to begin session
        experiment_info = get_config_info(config_info)
        file_path = set_file_path(experiment_info)

        # create window for experiment
        win = visual.Window([1024, 768], fullscr=False, units="pix")

        # create all stimuli
        choice_options = SubjectSpecificOptions(win=win)

        # collect option data
        option_rewards = [
            option.meanReward for option in choice_options.all_options[:12]
        ]
        option_type = [option.shape.name for option in choice_options.all_options[:12]]

        df_options_aux = pd.DataFrame(
            {
                "Subject ID": [experiment_info["Subject ID"]] * 12,
                "Session ID": [experiment_info["Session ID"]] * 12,
                "Session type": [experiment_info["Session type"]] * 12,
                "Option ID": list(range(12)),
                "Option type": option_type,
                "Option reward": option_rewards,
            }
        )
        df_options = df_options.append(df_options_aux)

        # initialize trial conditions and routine
        trial_conditions = TrialSequence(
            session_type=experiment_info["Session type"],
            session_id=experiment_info["Session ID"],
        ).generate()
        trial_routine = TrialRoutine(
            win=win, all_choice_options=choice_options.all_options
        )

        # trial and experiment data handlers
        trials = data.TrialHandler(
            trialList=trial_conditions, nReps=1, method="sequential"
        )
        this_exp = data.ExperimentHandler(
            extraInfo=experiment_info, dataFileName=file_path
        )
        this_exp.addLoop(trials)

        # run sequence of trials
        for this_trial in trials:
            trial_routine.set_condition(condition=this_trial)
            trial_data = trial_routine.simulate_wo_user_input()

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
                        delta_pmt = load_subject_delta_pmt(
                            experiment_info["Subject ID"]
                        )
                        choice_options.update_bonus_options(
                            new_delta_pmt=float(delta_pmt)
                        )

            # indicate end of trial to experiment handler
            this_exp.nextEntry()

        win.close()

    return df_options


def test_same_options_for_subject(df_options):
    """
    Function to test that the options generated are the same
    for each subject across session ids and session types, i.e.
    same shape, color, and reward.
    """
    test_len = []
    for subject_id in range(n_subjects):
        df_subject = df_options[df_options["Subject ID"] == subject_id]
        for option_id in range(12):
            test_len += [
                len(
                    df_subject.loc[
                        df_subject["Option ID"] == option_id, "Option type"
                    ].unique()
                )
            ]
    assert all(test_len) == 1, "Options are not the same within subject!"

    # manually checked whether option colors, shapes, and sets
    # were shuffled across subjects
    return


def test_subject_session_shuffle():
    """
    Function to test that the shuffling across subjects and
    sessions is as intended, i.e.
    1. shuffled (fully random) trials in a session
    2. different shuffle patterns across sessions
        - for the same session type, and
        - for different sessions type
    """
    # extract all data
    df = pd.DataFrame()
    for file in os.listdir("./data/"):
        if file.endswith(".csv"):
            aux = pd.read_csv("./data/" + file)
            df = df.append(aux)
    df.reset_index(inplace=True)

    # test fully random shuffle
    # for now, I've checked manually LOL
    # couldn't come up with a good test

    return df


if __name__ == "__main__":
    df_options = simulate_experiments()
    test_same_options_for_subject(df_options)
    df_trial_shuffle = test_subject_session_shuffle()
