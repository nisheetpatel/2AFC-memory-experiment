from pathlib import Path
from psychopy import core, data, gui
import random
import numpy as np


def display_config_window() -> gui.Dlg:
    """
    Shows GUI to user to input subject and session related information.
    """
    # define fields to show in gui
    dialog = gui.Dlg(title="Memory Experiment")
    dialog.addText("Subject Settings")
    dialog.addField("Subject ID")
    dialog.addText("Session Settings")
    dialog.addField("Session ID")
    dialog.addField("Session Type", choices=["practice", "training", "testing"])

    # show dialog and wait for OK or Cancel
    dialog_window_data = dialog.show()

    # shut down if user hit cancel
    if not dialog.OK:
        print("\nUser cancelled!\n")
        core.quit()

    return dialog_window_data


def get_config_info(dialog_window, set_seeds=True) -> dict:
    """
    Extracts information input by user into the gui into a dictionary.
    """
    experiment_info = {
        "Subject ID": dialog_window[0],
        "Session ID": dialog_window[1],
        "Session type": dialog_window[2],
    }

    # add date to info
    experiment_info["dateStr"] = data.getDateStr()

    # set seeds for experiment subject and session
    if set_seeds:
        subject_seed = int(experiment_info["Subject ID"])
        session_seed = int(experiment_info["Session ID"]) + 10 * subject_seed
        testing_seed = int(experiment_info["Session type"] == "testing") * 1000

        random.seed(subject_seed)
        np.random.seed(session_seed + testing_seed)

    return experiment_info


def set_file_path(experiment_info: dict) -> str:
    Path("./data").mkdir(parents=True, exist_ok=True)
    filename = "data/subj_{}_sess_{}_{}_{}".format(*experiment_info.values())
    return filename


def save_subject_delta_pmt(delta_pmt: float, subject_id: int) -> None:
    Path("./data").mkdir(parents=True, exist_ok=True)
    with open(f"./data/subj_{subject_id}.npy", "wb") as f:
        np.save(f, delta_pmt)
    return


def load_subject_delta_pmt(subject_id: int) -> float:
    try:
        with open(f"./data/subj_{subject_id}.npy", "rb") as f:
            delta_pmt = np.load(f)
    except FileNotFoundError:
        print(
            "\nTest sessions must start with session id = 0 "
            "to ensure adaptive testing for each subject!\n"
        )
        core.quit()

    return delta_pmt
