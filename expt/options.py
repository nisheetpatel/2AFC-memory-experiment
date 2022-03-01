from abc import ABC
from dataclasses import dataclass
import random
from typing import List
from psychopy import visual
from expt.stimuli import Stimuli
import numpy as np


@dataclass
class OnScreenObject(ABC):
    """Visual objects displayed on the screen."""

    win: visual.Window
    shape: visual
    # position: List[int, int]

    # def _set_position(self):
    #     self.shape.setPos(self.position)

    def set_position(self, newPos):
        # Set object position to one of left or right
        assert newPos in ["left", "right"]

        if newPos == "left":
            self.shape.setPos([-200, 0])
        elif newPos == "right":
            self.shape.setPos([200, 0])

    def _get_position(self):
        # Fetch object position
        return self.shape.pos


@dataclass
class ChoiceOption(OnScreenObject):
    """Standard choice option for 2AFC task."""

    meanReward: float
    stdReward: float

    def generate_reward(self):
        r = np.random.normal(self.meanReward, self.stdReward)
        return r


@dataclass
class ShapeOption(ChoiceOption):
    """Standard choice option for 2AFC task."""

    shape: visual.ShapeStim
    stdReward: float = 1

    def __str__(self):
        return f"{self.shape.color}_{str(self.shape)}"


class BonusOption(ChoiceOption):
    """Numerical bonus choice option for 2AFC task."""

    def __init__(self, win, meanReward):
        self.stdReward: float = 0
        self.shape = visual.TextStim(
            win,
            text=str(np.around(meanReward, 1)),
            font="Open Sans",
            color="black",
            height=80,
        )
        self.win = win
        self.meanReward = meanReward


class FixCross(OnScreenObject):
    """Fixation cross for 2AFC task."""

    def __init__(self, win):
        self.win = win
        self.shape = visual.ShapeStim(
            win=self.win,
            size=10,
            vertices="cross",
            lineColor="white",
            fillColor="white",
        )


class FeedbackRect(OnScreenObject):
    """Feedback rectangle indicating subject's"""

    def __init__(self, win):
        self.win = win
        self.shape = visual.Polygon(
            win=self.win,
            edges=4,
            ori=45,
            size=250,
            lineColor="black",
            fillColor=None,
            colorSpace="rgb",
        )


class FeedbackText(OnScreenObject):
    """Feedback text indicating reward obtained."""

    def __init__(self, win, rewardObtained, pos=None):
        self.win = win
        self.rewardObtained = rewardObtained
        self.shape = visual.TextBox2(
            win=self.win,
            text=f"$ {np.around(self.rewardObtained,1)}",
            font="Open Sans",
            color="black",
            alignment="center",
        )
        if pos is not None:
            self.set_position(newPos=pos)

    def set_position(self, newPos):
        # Set object position to one of left or right
        assert newPos in ["left", "right"]

        if newPos == "left":
            self.shape.setPos([0, 120])
        elif newPos == "right":
            self.shape.setPos([400, 120])


@dataclass
class OptionSet:
    """
    A set of 3 options with specific stakes,
    relative frequency of occurance, and color.
    """

    win: visual.Window
    stakes: float
    freq: int
    color: str
    setN: str
    meanReward: float = 10

    def __post_init__(self):
        assert self.setN in ["set1", "set2", "set3", "set4"]

        stimuli = Stimuli(win=self.win, color=self.color)
        stimSet = stimuli.get_stim_set(setN=self.setN)

        rewards = [
            self.meanReward + self.stakes,
            self.meanReward,
            self.meanReward - self.stakes,
        ]

        self.options = []
        for stim, reward in zip(stimSet, rewards):
            self.options.append(ShapeOption(self.win, shape=stim, meanReward=reward))


def create_choice_options(win) -> List[ChoiceOption]:
    """
    Function to create choice options for a subject.
    Deprecated: does not support adaptive setting of Delta_PMT.
    """
    # create shuffled lists of sets and colors
    set_names = ["set1", "set2", "set3", "set4"]
    random.shuffle(set_names)
    colors = ["red", "yellow", "blue", "green"]
    random.shuffle(colors)
    stakes = [4, 1, 4, 1]
    freqs = [4, 4, 1, 1]

    # Create 4 sets of 3 options each
    shape_options = []
    for setN, color, stake, freq in zip(set_names, colors, stakes, freqs):
        shape_options += OptionSet(
            win, setN=setN, color=color, stakes=stake, freq=freq
        ).options

    # Bonus choice options (as numbers shown on screen)
    good_bonus_options = []
    bad_bonus_options = []
    for option in shape_options:

        good_bonus_options.append(
            BonusOption(win=win, meanReward=(option.meanReward + 2))
        )
        bad_bonus_options.append(
            BonusOption(win=win, meanReward=(option.meanReward - 2))
        )

    choice_options = shape_options + good_bonus_options + bad_bonus_options

    return choice_options


@dataclass
class SubjectSpecificOptions:
    """
    Regular shape-based and bonus choice options for a given subject.
    """

    win: visual.Window
    delta_pmt: float = 4
    set_names = ["set1", "set2", "set3", "set4"]
    colors = ["red", "yellow", "blue", "green"]
    stakes = [4, 1, 4, 1]
    freqs = [4, 4, 1, 1]

    # parameters for adaptive setting of delta_pmt
    a = 0.16
    b = 0.84
    decay = 1
    counter = 0
    n_adaptive_trials = 20

    def __post_init__(self):
        """Creates all shape-based options and bonus options"""
        # shuffle the sets and colors
        random.shuffle(self.set_names)
        random.shuffle(self.colors)

        # Create 4 sets of 3 options each
        self.shape_options = []
        for setN, color, stake, freq in zip(
            self.set_names, self.colors, self.stakes, self.freqs
        ):
            self.shape_options += OptionSet(
                self.win, setN=setN, color=color, stakes=stake, freq=freq
            ).options

        # Bonus choice options (as numbers shown on screen)
        self.good_bonus_options = []
        self.bad_bonus_options = []
        for option in self.shape_options:

            self.good_bonus_options.append(
                BonusOption(
                    win=self.win, meanReward=(option.meanReward + self.delta_pmt)
                )
            )
            self.bad_bonus_options.append(
                BonusOption(
                    win=self.win, meanReward=(option.meanReward - self.delta_pmt)
                )
            )

        self.all_options = (
            self.shape_options + self.good_bonus_options + self.bad_bonus_options
        )
        return

    def update_bonus_options(self, change_in_delta=0, new_delta_pmt=None) -> float:
        if (new_delta_pmt is not None) & (change_in_delta == 0):
            change_in_delta = new_delta_pmt - self.delta_pmt

        for option in self.good_bonus_options:
            option.meanReward += change_in_delta
            option.shape.text = str(np.around(option.meanReward, 1))

        for option in self.bad_bonus_options:
            option.meanReward -= change_in_delta
            option.shape.text = str(np.around(option.meanReward, 1))
        return

    def adapt_delta(self, correct) -> None:
        self.counter += 1

        # decay for second half of adaptive trials
        if self.counter > self.n_adaptive_trials / 2:
            self.decay = max(2 * (1 - self.counter / self.n_adaptive_trials), 0)

        # continuous adaptive setting
        if correct:
            change_in_delta = -self.a * self.decay
        else:
            change_in_delta = self.b * self.decay

        # reset mean reward of bonus options and the delta_pmt attribute
        # in class based on new value of delta_pmt
        self.delta_pmt += change_in_delta
        self.update_bonus_options(change_in_delta)
        return self.delta_pmt


position = {
    "left": [-200, 0],
    "right": [200, 0],
    "center": [0, 0],
    "top-left": [0, 120],
    "top-right": [400, 120],
}


def set_stimulus_position(
    stimulus: OnScreenObject, position: List[int] = position["center"]
) -> None:
    # Sets the position of the stimulus to pre-defined left or right positions
    stimulus.shape.setPos(position)
    return
