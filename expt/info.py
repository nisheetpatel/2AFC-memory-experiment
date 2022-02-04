from psychopy import core, data, gui
import random
import numpy as np


def define_dialog_config_window() -> gui.Dlg:
    """
    Shows GUI to user to input subject and session related information.
    """
    dialog = gui.Dlg(title="Memory Experiment")
    dialog.addText("Subject Settings")
    dialog.addField("Subject ID")
    dialog.addText("Session Settings")
    dialog.addField("Session ID")
    dialog.addField("Session Type", choices=["practice", "training", "testing"])
    dialog.addField(
        "Instruction set", choices=["first session", "this ain't yo mama's first rodeo"]
    )

    ok_data = dialog.show()  # show dialog and wait for OK or Cancel

    if dialog.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print("\nUser cancelled!\n")
        core.quit()

    return dialog


def get_info_from_config_window(dialog_window, set_seeds=True) -> dict:
    """
    Extracts information input by user into the gui into a dictionary.
    """
    experiment_info = {
        "Subject ID": dialog_window.data[0],
        "Session ID": dialog_window.data[1],
        "Session type": dialog_window.data[2],
    }

    # add date to info
    experiment_info["dateStr"] = data.getDateStr()

    # set seeds for experiment subject and session
    if set_seeds:
        random.seed(int(experiment_info["Subject ID"]))
        testing_seed = 100 * int(experiment_info["Session type"] == "testing")
        np.random.seed(int(experiment_info["Session ID"]) + testing_seed)

    return experiment_info
