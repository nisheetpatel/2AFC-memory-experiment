from dataclasses import dataclass
from expt.options import FixCross, FeedbackRect, FeedbackText
from psychopy import visual, core, event


@dataclass
class TrialRoutine:
    """The 2AFC trial routine."""

    # condition: dict
    win: visual.Window
    all_choice_options: list
    clock = core.Clock()

    def __post_init__(self):
        self.fixCross = FixCross(self.win)
        self.feedbackRect = FeedbackRect(self.win)

    def set_condition(self, condition: dict) -> None:
        assert "option_a", "option_b" in condition
        self.condition = condition

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
        outcome_reward = self.trial_choices[responses.index(response)].generateReward()

        return outcome_correct, outcome_reward

    def run(self) -> tuple:
        """
        Run the full trial routine.
        Returns 2 tuples containing the data keys and values:
        response, reaction time, correct, reward
        """
        # Assign choice options for the trial
        self._assign_choice_options()

        # Show fixation cross and wait 1 second
        self.fixCross.shape.draw()
        self.win.flip()
        core.wait(1)

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
        self.feedbackRect.set_position(newPos=resp)
        self.feedbackRect.shape.draw()
        feedbackText = FeedbackText(self.win, rew, pos=resp)
        feedbackText.shape.draw()
        self.win.flip()
        core.wait(1)

        # Inter-trial interval
        self.win.flip()
        core.wait(0.5)

        # defining quantities to return
        data_keys = ("response", "reaction_time", "correct", "reward")
        data_values = (resp, rt, corr, rew)

        return data_keys, data_values
