from dataclasses import dataclass
from psychopy import visual
import random


@dataclass
class Stimuli:
    """Generates psychopy shapeStim objects"""

    win: visual.Window
    color: str
    lineColor: str = "black"
    colorSpace: str = "rgb"
    stimSize: int = 100

    def __post_init__(self):
        # define twelve shapes to choose from
        self.hexagon = visual.Polygon(
            win=self.win,
            edges=6,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.triangle = visual.Polygon(
            win=self.win,
            edges=3,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.diamond = visual.Polygon(
            win=self.win,
            edges=4,
            size=[self.stimSize, self.stimSize / 2],
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.rectangle = visual.Polygon(
            win=self.win,
            edges=4,
            size=self.stimSize,
            ori=-45,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.oval = visual.Circle(
            win=self.win,
            radius=[self.stimSize / 4, self.stimSize / 2],
            lineColor=self.lineColor,
            fillColor=self.color,
        )

        self.star = visual.ShapeStim(
            win=self.win,
            vertices="star7",
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
        )

        self.cross = visual.ShapeStim(
            win=self.win,
            vertices="cross",
            size=self.stimSize,
            ori=45,
            lineColor=self.lineColor,
            fillColor=self.color,
        )

        self.pentagon = visual.Polygon(
            win=self.win,
            edges=5,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.circle = visual.Circle(
            win=self.win,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.heptagon = visual.Polygon(
            self.win,
            edges=7,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

        self.plus = visual.ShapeStim(
            self.win,
            vertices="cross",
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
        )

        self.pacman = visual.Pie(
            win=self.win,
            size=self.stimSize,
            start=60,
            end=-240,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
        )

    def getStimSet(self, setN):
        # generate a set of three stimulus shapes
        assert setN in ["set1", "set2", "set3", "set4"]

        if setN == "set1":
            stims = [self.heptagon, self.triangle, self.cross]

        elif setN == "set2":
            stims = [self.rectangle, self.circle, self.star]

        elif setN == "set3":
            stims = [self.diamond, self.pentagon, self.oval]

        elif setN == "set4":
            stims = [self.hexagon, self.plus, self.pacman]

        random.shuffle(stims)

        return stims
