from dataclasses import dataclass
from dataclasses import dataclass
from psychopy import visual
from pygame import font


@dataclass
class Instructions:
    win: visual.Window
    session_type: str
    instruction_set: str

    def __post_init__(self):
        if self.session_type == "practice":
            instruction_text = "Practice session"
        elif self.session_type == "training":
            instruction_text = "Training session"
        elif self.session_type == "testing":
            instruction_text = "Testing session"
        if self.instruction_set == "first session":
            instruction_text_2 = "Instructions"

        self.shape = visual.TextStim(
            win=self.win, text=instruction_text, color="black", font="Open Sans"
        )
        self.shape2 = visual.TextStim(
            win=self.win, text=instruction_text_2, color="black", font="Open Sans"
        )
