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
    stimSize: int = 0.3
    units: str = "height"

    def __post_init__(self):
        # define twelve shapes to choose from
        self.hexagon = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=6,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-hexagon",
        )

        self.triangle = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=3,
            ori=90,
            size=self.stimSize * 1.1,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-triangle",
        )

        self.diamond = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=4,
            size=[self.stimSize, self.stimSize / 2],
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-diamond",
        )

        self.rectangle = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=4,
            size=self.stimSize * 1.1,
            ori=-45,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-rectangle",
        )

        self.oval = visual.Circle(
            win=self.win,
            units=self.units,
            radius=[self.stimSize / 4.1, self.stimSize / 2.1],
            lineColor=self.lineColor,
            fillColor=self.color,
            name=f"{self.color}-oval",
        )

        self.star = visual.ShapeStim(
            win=self.win,
            units=self.units,
            vertices="star7",
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            name=f"{self.color}-star",
        )

        self.cross = visual.ShapeStim(
            win=self.win,
            units=self.units,
            vertices="cross",
            size=self.stimSize,
            ori=45,
            lineColor=self.lineColor,
            fillColor=self.color,
            name=f"{self.color}-cross",
        )

        self.pentagon = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=5,
            size=self.stimSize * 1.05,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-pentagon",
        )

        self.circle = visual.Circle(
            win=self.win,
            units=self.units,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-circle",
        )

        self.heptagon = visual.Polygon(
            win=self.win,
            units=self.units,
            edges=7,
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-heptagon",
        )

        self.plus = visual.ShapeStim(
            win=self.win,
            units=self.units,
            vertices="cross",
            size=self.stimSize,
            lineColor=self.lineColor,
            fillColor=self.color,
            name=f"{self.color}-plus",
        )

        self.pacman = visual.Pie(
            win=self.win,
            units=self.units,
            size=self.stimSize,
            start=60,
            end=-240,
            lineColor=self.lineColor,
            fillColor=self.color,
            colorSpace=self.colorSpace,
            name=f"{self.color}-pacman",
        )

    def get_stim_set(self, setN):
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
