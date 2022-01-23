from dataclasses import dataclass
from expt.options import FixCross, FeedbackRect, FeedbackText
from psychopy import visual, core, event
import random


@dataclass
class TrialRoutine:
    """The 2AFC trial routine."""

    condition: dict
    win: visual.Window
    allOptions: list
    clock = core.Clock()

    def __post_init__(self):
        self.fixCross = FixCross(self.win)
        self.feedbackRect = FeedbackRect(self.win)

    def assignChoiceOptions(self):
        """
        Get the relevant choice options for the
        trial condition and set their positions.
        """
        # assign left and right stimuli
        self.choiceOpt1 = self.allOptions[self.condition["sA"]]
        self.choiceOpt2 = self.allOptions[self.condition["sB"]]
        self.choiceOptions = [self.choiceOpt1, self.choiceOpt2]
        random.shuffle(self.choiceOptions)

        # set position
        self.choiceOptions[0].setPosition(newPos="left")
        self.choiceOptions[1].setPosition(newPos="right")

    def outcome(self, response):
        """Whether the response was correct or not and reward obtained."""
        # mean rewards for both choice options
        optRewards = [opt.meanReward for opt in self.choiceOptions]

        # get index of higher reward
        maxR = max(optRewards)
        maxR_idx = optRewards.index(maxR)

        # identify and return correct response
        responses = ["left", "right"]
        correctResponse = responses[maxR_idx]
        outcomeCorr = response == correctResponse

        # outcome reward
        outcomeRew = self.choiceOptions[responses.index(response)].generateReward()

        return outcomeCorr, outcomeRew

    def run(self):
        """
        Run the full trial routine.
        """
        # Assign choice options for the trial
        self.assignChoiceOptions()

        # Show fixation cross and wait 1 second
        self.fixCross.shape.draw()
        self.win.flip()
        core.wait(1)

        # Show choice options
        for opt in self.choiceOptions:
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
        for opt in self.choiceOptions:
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


class SessionRoutine:
    pass
