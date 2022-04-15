from dataclasses import dataclass
from dataclasses import dataclass
from psychopy import visual, event
import numpy as np

@dataclass
class ScreenText:
    """Fullscreen text to be displayed."""

    # condition: dict
    win: visual.Window
    message: str

    def show(self):
        # display instructions and wait
        message1 = visual.TextStim(
            self.win,
            text=self.message,
            height=0.075,
            units="height",
            wrapWidth=1.25,
        )
        message1.draw()
        self.win.flip()  # to show our newly drawn 'stimuli'

        # pause until there's a keypress
        _ = event.waitKeys()
        self.win.flip()


@dataclass
class BeginSessionScreen(ScreenText):
    message: str = "Press any key when ready"


@dataclass
class EndSessionScreen(ScreenText):
    message: str = "Please take a break.\n Press any key when ready for the next step."


@dataclass
class EndOfExperimentDayScreen(ScreenText):
    message: str = "You are done for the day.\n\nPress any key to view your earnings."


@dataclass
class TotalEarningsScreen:
    win: visual.Window
    payoff_list: list
    
    def _create_text_stims(self):
        
        kwargs = {"win":self.win, "height":0.03, "units":"height"}
        y = np.arange(30, -40, -6)/100
        text_stims = []

        # show up fee
        text_stims += [visual.TextStim(text=f"Show up fee", pos=(-0.2, 0.36), **kwargs)]
        text_stims += [visual.TextStim(text="$25.0", pos=(0.2, 0.36), **kwargs)]

        # session payoffs
        for idx, payoff in enumerate(self.payoff_list):
            text_stims += [visual.TextStim(text=f"Selected trial {idx+1}", pos=(-0.2, y[idx]), **kwargs)]
            text_stims += [visual.TextStim(text=f"${round(payoff, ndigits=1)}", pos=(0.2, y[idx]), **kwargs)]

        # totals
        total = round(25 + sum(self.payoff_list), 1)
        kwargs["height"] = 0.04
        text_stims += [visual.TextStim(text=f"Total", pos=(-0.2, -0.06), **kwargs)]
        text_stims += [visual.TextStim(text=f"${total}", pos=(0.2, -0.06), **kwargs)]
        
        text_stims += [visual.TextStim(text="Press space to end experiment", pos=(0, -0.3), **kwargs)]

        text_stims += [visual.Line(win=self.win, start=(0.3, -0.03), end=(-0.3, -0.03), lineWidth=0.05, color="beige", units="height")]

        return text_stims

    def show(self):
        text_stims = self._create_text_stims()
        for text_stim in text_stims:
            text_stim.draw()
        self.win.flip()
        event.waitKeys(keyList=["space"])