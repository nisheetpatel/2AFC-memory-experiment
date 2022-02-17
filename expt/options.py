from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
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

    def setPosition(self, newPos):
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

    def generateReward(self):
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
            text=str(meanReward),
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
            text=f"$ {np.around(self.rewardObtained,2)}",
            font="Open Sans",
            color="black",
            alignment="center",
        )
        if pos is not None:
            self.setPosition(newPos=pos)

    def setPosition(self, newPos):
        # Set object position to one of left or right
        assert newPos in ["left", "right"]

        if newPos == "left":
            self.shape.setPos([0, 120])
        elif newPos == "right":
            self.shape.setPos([400, 120])


@dataclass
class OptionSet:
    """
    Defines a set of 3 options with specific stakes,
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
        stimSet = stimuli.getStimSet(setN=self.setN)

        rewards = [
            self.meanReward + self.stakes,
            self.meanReward,
            self.meanReward - self.stakes,
        ]

        self.options = []
        for stim, reward in zip(stimSet, rewards):
            self.options.append(ShapeOption(self.win, shape=stim, meanReward=reward))


def create_choice_options(win):

    # Standard choice options (shape stimuli)
    # Create 4 sets of 3 options each
    optSet1 = OptionSet(win, setN="set1", color="red", stakes=4, freq=4)
    optSet2 = OptionSet(win, setN="set2", color="yellow", stakes=1, freq=4)
    optSet3 = OptionSet(win, setN="set3", color="blue", stakes=4, freq=1)
    optSet4 = OptionSet(win, setN="set4", color="green", stakes=1, freq=1)

    shape_options = (
        optSet1.options + optSet2.options + optSet3.options + optSet4.options
    )

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
