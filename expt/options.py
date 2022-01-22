from abc import ABC
from dataclasses import dataclass
from psychopy import visual
from expt.stimuli import Stimuli
import numpy as np

@dataclass
class OnScreenObject(ABC):
    """Visual objects displayed on the screen."""
    win: visual.Window
    shape: visual

    def setPosition(self, newPos):
        # Set object position to one of left or right
        assert newPos in ['left', 'right']

        if newPos == 'left':
            self.shape.setPos([-200, 0])
        elif newPos == 'right':
            self.shape.setPos([200, 0])

    def getPosition(self):
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
class Option(ChoiceOption):
    """Standard choice option for 2AFC task."""
    shape: visual.ShapeStim
    stdReward: float = 1


@dataclass
class BonusOption(ChoiceOption):
    """Numerical bonus choice option for 2AFC task."""
    shape: visual.TextStim
    stdReward: float = 0


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
        assert self.setN in ['set1','set2','set3','set4']
        
        stimuli = Stimuli(win=self.win, color=self.color)
        stims = stimuli.getStimSet(setN=self.setN)

        rewards = [self.meanReward + self.stakes,
                self.meanReward,
                self.meanReward - self.stakes]
        
        self.options = []
        for stim, reward in zip(stims,rewards):
            self.options.append(Option(self.win, shape=stim, meanReward=reward))


def createAllOptionSets(win):
    # Create 4 sets of 3 options each

    optSet1 = OptionSet(win, setN='set1', color='red',
                        stakes=4, freq=4)
    optSet2 = OptionSet(win, setN='set2', color='yellow',
                        stakes=1, freq=4)
    optSet3 = OptionSet(win, setN='set3', color='blue',
                        stakes=4, freq=1)
    optSet4 = OptionSet(win, setN='set4', color='green',
                        stakes=1, freq=1)

    return optSet1, optSet2, optSet3, optSet4



class fixCross(OnScreenObject):
    """Fixation cross for 2AFC task."""
    def __init__(self, win):
        self.win = win
        self.shape = visual.ShapeStim(win=self.win,
                                size=10, 
                                vertices='cross',
                                lineColor='white',
                                fillColor='white')


class feedbackRect(OnScreenObject):
    """Feedback rectangle indicating subject's"""
    def __init__(self, win):
        self.win = win
        self.shape = visual.Polygon(win=self.win,
                                edges=4, ori=45,
                                size=250,
                                lineColor='black',
                                fillColor=None,
                                colorSpace='rgb')


class feedbackText(OnScreenObject):
    """Feedback text indicating reward obtained."""
    def __init__(self, win, rewardObtained):
        self.win = win
        self.rewardObtained = rewardObtained
        self.shape = visual.TextBox2(win=self.win,
                    text=f"$ {np.around(self.rewardObtained,2)}",
                    font='Open Sans', color='black', alignment='center')

    def setPosition(self, newPos):
        # Set object position to one of left or right
        assert newPos in ['left', 'right']

        if newPos == 'left':
            self.shape.setPos([0, 120])
        elif newPos == 'right':
            self.shape.setPos([400, 120])