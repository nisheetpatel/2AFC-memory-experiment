from dataclasses import dataclass
from expt.options import create_choice_options, FixCross, FeedbackRect, FeedbackText
from psychopy import visual, core, event


@dataclass
class TrialRoutine:
    """The 2AFC trial routine."""

    condition: dict
    win: visual.Window
    clock = core.Clock()

    def __post_init__(self):
        self.choice_options = create_choice_options(self.win)
        self.fixCross = FixCross(self.win)
        self.feedbackRect = FeedbackRect(self.win)

    def assign_choice_options(self):
        """
        Get the relevant choice options for the
        trial condition and set their positions.
        """
        # assign left and right stimuli
        self.option_a = self.choice_options[self.condition["option_a"]]
        self.option_b = self.choice_options[self.condition["option_b"]]
        self.choice_options = [self.option_a, self.option_b]

        # set position
        self.choice_options[0].setPosition(newPos="left")
        self.choice_options[1].setPosition(newPos="right")

    def outcome(self, response):
        """Whether the response was correct or not and reward obtained."""
        # mean rewards for both choice options
        option_rewards = [opt.meanReward for opt in self.choice_options]

        # get index of the option with higher reward
        idx_max_reward = option_rewards.index(max(option_rewards))

        # identify and return correct response
        responses = ["left", "right"]
        correct_response = responses[idx_max_reward]
        outcome_correct = response == correct_response

        # outcome reward
        outcome_reward = self.choice_options[responses.index(response)].generateReward()

        return outcome_correct, outcome_reward

    def run(self):
        """
        Run the full trial routine.
        """
        # Assign choice options for the trial
        self.assign_choice_options()

        # Show fixation cross and wait 1 second
        self.fixCross.shape.draw()
        self.win.flip()
        core.wait(1)

        # Show choice options
        for opt in self.choice_options:
            opt.shape.draw()
        self.win.flip()

        # Reset clock to zero
        self.clock.reset()

        # record response, response time, and correct
        keys = event.waitKeys(keyList=["left", "right", "escape"])
        rt = self.clock.getTime()
        resp = keys[0]
        corr, rew = self.outcome(response=resp)

        # show feedback with choice options
        for opt in self.choice_options:
            opt.shape.draw()
        self.feedbackRect.setPosition(newPos=resp)
        self.feedbackRect.shape.draw()
        feedbackText = FeedbackText(self.win, rew, pos=resp)
        feedbackText.shape.draw()
        self.win.flip()
        core.wait(1)

        # Inter-trial interval
        self.win.flip()
        core.wait(1)

        return rt, resp, corr, rew
