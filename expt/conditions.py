from dataclasses import dataclass
import numpy as np


@dataclass
class TrialSequenceGenerator:
    session_type: str
    n_bonus_trials_per_option: int = 4

    def __post_init__(self):
        if self.session_type == "practice":
            self.n_trials_per_session = 12
            self.rel_freq = 1
        elif self.session_type in ["training", "testing"]:
            self.n_trials_per_session = 180
            self.rel_freq = 4

    @property
    def trial_type_distribution(self):
        # weighted list of trial conditions
        condition_distributiuon = list(
            np.append(np.repeat(np.arange(6), self.rel_freq), np.arange(6, 12), axis=0)
        )
        np.random.shuffle(condition_distributiuon)

        return condition_distributiuon

    @property
    def n_repeats(self):
        # number of times the weighted conditions are repeated
        return int(self.n_trials_per_session / len(self.trial_type_distribution))

    def get_options_for_condition(self, condition):
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

    def add_bonus_trials(self, conditions):
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
        conditions = []
        for _ in range(self.n_repeats):
            conditions.extend(self.trial_type_distribution)

        # insert bonus trials for test sessions
        if self.session_type == "testing":
            conditions = self.add_bonus_trials(conditions)

        return conditions

    def conditions_dict(self, condition):
        choice_options = self.get_options_for_condition(condition)
        condition_dict_row = {
            "Condition": condition,
            "option_a": choice_options[0],
            "option_b": choice_options[1],
        }
        return condition_dict_row

    def generate(self):
        trial_sequence = list(map(self.conditions_dict, self.condition_sequence))
        return trial_sequence
