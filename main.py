from psychopy import visual, data
from expt.info import display_config_window, get_config_info
from expt.options import SubjectSpecificOptions
from expt.routines import DayRoutine, TrainingSession

if __name__ == "__main__":
    # initialize info to begin experiment for the day
    dialog_window = display_config_window()
    experiment_info = get_config_info(dialog_window)

    # create window for experiment
    win = visual.Window([1920, 1080], fullscr=True, units="pix", color=(-1, -1, -1))

    # create all stimuli
    choice_options = SubjectSpecificOptions(win=win)

    # session routine
    day_routine = DayRoutine(win=win, choice_options=choice_options, experiment_info=experiment_info)
    day_routine.run()
