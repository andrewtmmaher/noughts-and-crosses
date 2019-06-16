import numpy as np
from collections import Counter

ERROR_WEIGHT = 10
DRAW_MOVE_WEIGHT = 1
FINAL_VICTORY_PLACEMENT_WEIGHT = 10
VICTORY_LOSS_MODE_WEIGHT = 2


class GameRecorder(object):

    def __init__(
            self, placement_errors=None, correct_placements=None, winner=None):
        self.placement_errors = placement_errors or []
        self.correct_placements = correct_placements or []
        self.winner = winner or None

    def record_placement_error(self, player, board, position):
        self.placement_errors.append((player, position, *board))

    def record_correct_placement(self, player, board, position):
        self.correct_placements.append((player, position, *board))

    def record_winner(self, winner):
        self.winner = winner


class EpisodeRecorder(object):

    def __init__(self, records=None, winners=None):
        self.records = records or []
        self.winners = winners or []

    def snapshot_game(self, game_recorder):
        self.winners.append(game_recorder.winner)

        self.records.extend(
            [[-1 * ERROR_WEIGHT, *record]
             for record in game_recorder.placement_errors]
        )

        if game_recorder.winner is not None:

            self.records.extend(
                [[
                    VICTORY_LOSS_MODE_WEIGHT * record[0] * game_recorder.winner,
                    *record
                ]
                 for record in game_recorder.correct_placements[:-1]]
            )
            self.records.append([
                FINAL_VICTORY_PLACEMENT_WEIGHT,
                *game_recorder.correct_placements[-1]
            ])

        else:
            self.records.extend(
                [[DRAW_MOVE_WEIGHT, *record]
                 for record in game_recorder.correct_placements]
            )

    def finish_recording(self):
        self.records = np.array(self.records)

    def extract_boards(self, counter, position):
        return self.records[(self.records[:, 1] == counter)
                            & (self.records[:, 2] == position), 3:]

    def extract_weights(self, counter, position):
        return np.abs(
            self.records[(self.records[:, 1] == counter) & (self.records[:, 2] == position), 0]
        )

    def extract_labels(self, counter, position):
        return np.sign(
            self.records[(self.records[:, 1] == counter)
                         & (self.records[:, 2] == position), 0]
        )

    def print_metrics(self):
        winner_counter = Counter(self.winners)

        print('Crosses win fraction: {}'.format(
            winner_counter[1] / len(self.winners)))
        print('Noughts win fraction: {}'.format(
            winner_counter[-1] / len(self.winners)))
