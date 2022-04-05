from dataclasses import dataclass
import numpy as np


@dataclass
class TrialSequence:
    session_type: str
    session_id: int
    n_bonus_trials_per_option: int = 2
    n_trials_per_session = 90
    rel_freq = 4
    n_repeats = 3

    def __post_init__(self):
        if self.session_type == "practice":
            self.n_trials_per_session = 30
            self.n_repeats = 1
        elif self.session_type == "training":
            self.n_trials_per_session = 210
            self.n_repeats = 7

    @property
    def trial_conditions(self):
        # weighted list of trial conditions
        conditions = list(
            np.repeat(
                np.append(
                    np.repeat(np.arange(6), self.rel_freq), np.arange(6, 12), axis=0
                ),
                self.n_repeats,
            )
        )
        np.random.shuffle(conditions)

        return conditions

    def _get_options_for_condition(self, condition):
        # define option set for each condition
        if condition < 12:
            if condition % 3 == 0:
                choiceSet = [condition + 1, condition + 2]  # 1 v 2; PMT 0
            elif condition % 3 == 1:
                choiceSet = [condition - 1, condition + 1]  # 0 v 2; PMT 1
            else:
                choiceSet = [condition - 2, condition - 1]  # 0 v 1; PMT 2
        elif condition < 24:
            choiceSet = [condition - 12, condition]
        elif condition < 36:
            choiceSet = [condition - 24, condition]
        np.random.shuffle(choiceSet)
        return choiceSet

    def _add_bonus_trials(self, conditions):
        # function to insert bonus trials in given sequence
        for option_id in range(12):
            ids = [i for i in range(len(conditions)) if conditions[i] == option_id]
            np.random.shuffle(ids)
            idx_plus_Delta = ids[: int(self.n_bonus_trials_per_option / 2)]
            idx_minus_Delta = ids[
                int(self.n_bonus_trials_per_option / 2) : self.n_bonus_trials_per_option
            ]

            ids_both_Delta = idx_plus_Delta + idx_minus_Delta
            ids_both_Delta.sort(reverse=True)
            ids.sort()

            # indicate pmt trial and type
            for idx in ids_both_Delta:
                if idx in idx_plus_Delta:
                    conditions.insert(idx + 1, conditions[idx] + 12)
                elif idx in idx_minus_Delta:
                    conditions.insert(idx + 1, conditions[idx] + 24)

        return conditions

    @property
    def condition_sequence(self):
        # sequence of trial conditions
        conditions = self.trial_conditions

        # insert bonus trials for test sessions
        if self.session_type == "testing":
            conditions = self._add_bonus_trials(conditions)

        return conditions

    def _conditions_dict(self, condition):
        choice_options = self._get_options_for_condition(condition)
        condition_dict_row = {
            "Condition": condition,
            "option_a": choice_options[0],
            "option_b": choice_options[1],
        }
        return condition_dict_row

    def generate(self):
        trial_sequence = list(map(self._conditions_dict, self.condition_sequence))
        return trial_sequence
