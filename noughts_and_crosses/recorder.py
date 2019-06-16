import numpy as np
from collections import Counter


class GameRecorder(object):

    def __init__(self):
        self.placement_errors = []
        self.correct_placements = []
        self.winner = None

    def record_placement_error(self, player, board, position):
        self.placement_errors.append((player, position, *board))

    def record_correct_placement(self, player, board, position):
        self.correct_placements.append((player, position, *board))

    def record_winner(self, winner):
        self.winner = winner


class SeriesRecorder(object):

    def __init__(self):
        self.placement_errors = []
        self.correct_placements = []
        self.winners = []

    def snapshot_game(self, game_recorder):
        self.winners.append(game_recorder.winner)

        self.placement_errors.extend(
            [[-10, *record]
             for record in game_recorder.placement_errors]
        )

        if game_recorder.winner is not None:

            self.correct_placements.extend(
                [[2 * record[0] * game_recorder.winner, *record]
                 for record in game_recorder.correct_placements[:-1]]
            )
            self.correct_placements.append([10, *game_recorder.correct_placements[-1]])

        else:
            self.correct_placements.extend(
                [[1, *record] for record in game_recorder.correct_placements]
            )

    def extract_boards(self, counter, position):
        arr = np.array(self.placement_errors + self.correct_placements)
        return arr[(arr[:, 1] == counter) & (arr[:, 2] == position), 3:]

    def extract_weights(self, counter, position):
        arr = np.array(self.placement_errors + self.correct_placements)
        return np.abs(arr[(arr[:, 1] == counter) & (arr[:, 2] == position), 0])

    def extract_labels(self, counter, position):
        arr = np.array(self.placement_errors + self.correct_placements)
        return np.sign(arr[(arr[:, 1] == counter) & (arr[:, 2] == position), 0])

    def print_metrics(self):
        winner_counter = Counter(self.winners)

        print('Crosses win fraction: {}'.format(
            winner_counter[1] / len(self.winners)))
        print('Noughts win fraction: {}'.format(
            winner_counter[-1] / len(self.winners)))
