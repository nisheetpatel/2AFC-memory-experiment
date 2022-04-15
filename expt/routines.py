import random
import numpy as np
from dataclasses import dataclass
from expt.conditions import TrialSequence
from expt.info import load_subject_delta_pmt, save_subject_delta_pmt, set_file_path, set_random_seed
from expt.instructions import BeginSessionScreen, EndOfExperimentDayScreen, EndSessionScreen, TotalEarningsScreen
from expt.options import ChoiceOption, FixCross, FeedbackRect, FeedbackText, RespondFasterText, SubjectSpecificOptions
from psychopy import visual, core, event, data


@dataclass
class TrialRoutine:
    """The 2AFC trial routine."""

    # condition: dict
    win: visual.Window
    all_choice_options: list
    clock = core.Clock()
    fixation_time: float = 1
    feedback_time: float = 1
    inter_trial_interval: float = 1

    def __post_init__(self):
        self.fix_cross = FixCross(self.win)
        self.feedback_rect = FeedbackRect(self.win)
        self.respond_faster_text = RespondFasterText(self.win)

    def _set_trial_type(self) -> None:
        """Records whether the current trial is a bonus trial"""
        self.bonus_trial = False
        if self.condition["Condition"] > 11:
            self.bonus_trial = True

    def set_condition(self, condition: dict) -> None:
        assert "option_a", "option_b" in condition
        self.condition = condition
        self._set_trial_type()

    def _assign_choice_options(self) -> None:
        """
        Get the relevant choice options for the
        trial condition and set their positions.
        """
        # assign left and right stimuli
        self.option_a = self.all_choice_options[self.condition["option_a"]]
        self.option_b = self.all_choice_options[self.condition["option_b"]]
        self.trial_choices = [self.option_a, self.option_b]

        # set position
        self.trial_choices[0].set_position(newPos="left")
        self.trial_choices[1].set_position(newPos="right")

    def _outcome(self, response):
        """Whether the response was correct or not and reward obtained."""
        # mean rewards for both choice options
        option_rewards = [opt.meanReward for opt in self.trial_choices]

        # get index of the option with higher reward
        idx_max_reward = option_rewards.index(max(option_rewards))

        # identify and return correct response
        responses = ["left", "right"]
        correct_response = responses[idx_max_reward]
        outcome_correct = response == correct_response

        # outcome reward
        outcome_reward = self.trial_choices[responses.index(response)].generate_reward()

        return outcome_correct, outcome_reward

    def run(self) -> dict:
        """
        Run the full trial routine.
        Returns 2 tuples containing the data keys and values:
        response, reaction time, correct, reward
        """
        # Assign choice options for the trial
        self._assign_choice_options()

        # Show fixation cross and wait 1 second
        self.fix_cross.shape.draw()
        self.win.flip()
        core.wait(self.fixation_time)

        # Show choice options
        for opt in self.trial_choices:
            opt.shape.draw()
        self.win.flip()

        # Reset clock to zero
        self.clock.reset()

        # record response, response time, and correct
        keys = event.waitKeys(keyList=["left", "right", "escape"])
        rt = self.clock.getTime()
        resp = keys[0]
        if resp != "escape":
            corr, rew = self._outcome(response=resp)
        else:
            print("\nUser terminated the experiment!\n")
            core.quit()

        # show feedback with choice options
        for opt in self.trial_choices:
            opt.shape.draw()
        self.feedback_rect.set_position(newPos=resp)
        self.feedback_rect.shape.draw()
        feedback_text = FeedbackText(self.win, rew, pos=resp)
        feedback_text.shape.draw()
        if rt > 3:
            self.respond_faster_text.shape.draw()
        self.win.flip()
        core.wait(self.feedback_time)

        # Inter-trial interval
        self.win.flip()
        core.wait(self.inter_trial_interval)

        # defining quantities to return
        trial_data = {
            "response": resp,
            "reaction_time": rt,
            "correct": corr,
            "reward": rew,
            "bonus_trial": self.bonus_trial,
        }

        return trial_data

    def simulate_wo_user_input(self) -> dict:
        """
        Run the full trial routine without any keyboard input.
        Returns 2 tuples containing the data keys and values:
        response, reaction time, correct, reward
        """
        # Assign choice options for the trial
        self._assign_choice_options()

        # set auto response, response time, and correct
        rt = 0.1
        resp = "left"
        corr, rew = self._outcome(response=resp)

        # defining quantities to return
        trial_data = {
            "response": resp,
            "reaction_time": rt,
            "correct": corr,
            "reward": rew,
            "bonus_trial": self.bonus_trial,
        }

        return trial_data


@dataclass
class SessionRoutine:
    win: visual.Window
    choice_options: SubjectSpecificOptions
    session_info: dict
    session_id: int
    final_session = False
    session_type: str = None

    def __post_init__(self):
        self.session_payoff = []

        # screens to display at the beginning and end of sesions
        self.initial_screen = BeginSessionScreen(self.win)
        if not self.final_session:
            self.final_screen = EndSessionScreen(self.win)
        else:
            self.final_screen = EndOfExperimentDayScreen(self.win)

    def setup_session_info(self):
        # experiment info
        self.session_info["Session type"] = self.session_type
        self.session_info["Session ID"] = self.session_id
        self.session_info["DateTime"] = data.getDateStr()

        # set random seeds
        set_random_seed(self.session_info)
        
        # set path to save file
        file_path = set_file_path(self.session_info)

        # data handler for session
        self.data_handler = data.ExperimentHandler(extraInfo=self.session_info, dataFileName=file_path)

    def initialize_trials(self):
        """Initialize trial conditions and routine."""
        self.trial_conditions = TrialSequence(session_type=self.session_type, session_id=self.session_id).generate()
        self.trial_routine = TrialRoutine(win=self.win, all_choice_options=self.choice_options.all_options)

    def setup_data_handlers(self):
        """Setup handlers for data collection."""
        self.trials = data.TrialHandler(trialList=self.trial_conditions, nReps=1, method="sequential")
        self.data_handler.addLoop(self.trials)
        self.payoff_trial_index = np.random.choice(self.trials.nTotal, size=2, replace=False)

    def run_trial_sequence(self):
        """Run sequence of trials for the session."""
        for this_trial in self.trials:
            # run one trial
            self.trial_routine.set_condition(condition=this_trial)
            trial_data = self.trial_routine.run()

            # record data
            for data_key, data_value in trial_data.items():
                self.trials.addData(data_key, data_value)

            # record payoff for randomly set payoff trial
            if self.trials.thisIndex in self.payoff_trial_index:
                self.session_payoff += [trial_data["reward"]]

            # indicate end of trial to data handler
            self.data_handler.nextEntry()


    def run(self):
        self.setup_session_info()
        self.initialize_trials()
        self.setup_data_handlers()
        self.initial_screen.show()
        self.run_trial_sequence()
        self.final_screen.show()
        return self.session_payoff


@dataclass
class PracticeSession(SessionRoutine):
    session_type = "practice"


@dataclass
class TrainingSession(SessionRoutine):
    session_type = "training"


@dataclass
class TestingSession(SessionRoutine):
    session_type = "testing"


@dataclass
class AdaptiveTestingSession(SessionRoutine):
    session_type = "testing"
    session_id = 0

    def run_trial_sequence(self):
        """Run sequence of trials for the session."""
        for this_trial in self.trials:
            # run one trial
            self.trial_routine.set_condition(condition=this_trial)
            trial_data = self.trial_routine.run()

            # record data
            for data_key, data_value in trial_data.items():
                self.trials.addData(data_key, data_value)

            # adapt delta on each bonus trial
            if trial_data["bonus_trial"]:
                delta_pmt = self.choice_options.adapt_delta(
                    correct=trial_data["correct"]
                )

            # record payoff for randomly set payoff trial
            if self.trials.thisIndex in self.payoff_trial_index:
                self.session_payoff += [trial_data["reward"]]

            # indicate end of trial to data handler
            self.data_handler.nextEntry()
        
        # save final delta_pmt for subject at the end of the session
        save_subject_delta_pmt(delta_pmt, self.session_info["Subject ID"])


@dataclass
class DayRoutine:
    win: visual.Window
    choice_options: SubjectSpecificOptions
    experiment_info: dict

    def __post_init__(self):
        self.day = self.experiment_info["Day"]
        assert self.day in [1,2], "Input Day must be 1 or 2"
        self.setup_session_routines()

    def setup_session_routines(self):
        kwargs = {
            "win": self.win,
            "choice_options": self.choice_options,
            "session_info": self.experiment_info
        }

        if self.day == 1:
            self.session_routines = [
                TrainingSession(session_id=1, session_type="training", **kwargs),
                TrainingSession(session_id=2, session_type="training", **kwargs),
                AdaptiveTestingSession(session_id=0, session_type="testing", **kwargs),
                TestingSession(session_id=1, session_type="testing", **kwargs),
                TestingSession(session_id=2, session_type="testing", **kwargs),
                TestingSession(session_id=3, session_type="testing", **kwargs),
            ]

        elif self.day == 2:
            self.session_routines = [
                PracticeSession(session_id=1, session_type="practice", **kwargs),
                TestingSession(session_id=4, session_type="testing", **kwargs),
                TestingSession(session_id=5, session_type="testing", **kwargs),
                TestingSession(session_id=6, session_type="testing", **kwargs),
                TestingSession(session_id=7, session_type="testing", **kwargs),
                TestingSession(session_id=8, session_type="testing", **kwargs),
                TestingSession(session_id=9, session_type="testing", **kwargs),
                TestingSession(session_id=10, session_type="testing", **kwargs),
            ]
            
            # load delta_pmt from previous day's adaptive testing session
            delta_pmt = load_subject_delta_pmt(self.experiment_info["Subject ID"])
            self.choice_options.update_bonus_options(new_delta_pmt=delta_pmt)

    def run(self):
        """Run the full experiment day."""
        
        # run each session and collect randomly selected payoff
        payoff_list = []
        for session_routine in self.session_routines:
            session_payoff = session_routine.run()
            if session_routine.session_type == "testing":
                payoff_list += session_payoff

        # pick five trials at random 
        random.shuffle(payoff_list)
        payoff_list = payoff_list[:5]
        
        # display total earnings at the end of the day
        total_earnings_screen = TotalEarningsScreen(win=self.win, payoff_list=payoff_list)
        total_earnings_screen.show()

        # print on terminal
        print("\nEnd of experiment day!\n")