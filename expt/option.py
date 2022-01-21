from dataclasses import dataclass
from turtle import color
from psychopy import visual
from expt.stimuli import Stimuli
import numpy as np


@dataclass
class Option:
    """Standard choice option for 2AFC task."""
    shape: visual.ShapeStim
    meanReward: float
    stdReward: float = 1

    def setPosition(self, newPos):
        self.shape.setPos(newPos)

    def generateReward(self):
        r = np.random.normal(self.meanReward, self.stdReward)
        return r


@dataclass
class OptionSet:
    """
    Defines a set of 3 options with specific stakes,
    relative frequency of occurance, and color.
    """
    win: visual.Window
    stakes: float
    relativeOccuranceFreq: int
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
            self.options.append(Option(shape=stim,meanReward=reward))


def createAllOptionSets(win):
    """
    Creates 4 sets of 3 options each.
    """
    optSet1 = OptionSet(win, color='red',
        stakes=4, relativeOccuranceFreq=4, setN='set1')
    optSet2 = OptionSet(win, color='yellow',
        stakes=1, relativeOccuranceFreq=4, setN='set2')
    optSet3 = OptionSet(win, color='blue',
        stakes=4, relativeOccuranceFreq=1, setN='set3')
    optSet4 = OptionSet(win, color='green',
        stakes=1, relativeOccuranceFreq=1, setN='set4')

    return optSet1, optSet2, optSet3, optSet4