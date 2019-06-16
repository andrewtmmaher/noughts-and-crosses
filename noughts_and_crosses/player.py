from position_strategy import (
    RandomPositionSelector, MlPositionSelector)


class Player(object):

    def __init__(self, counter, position_strategy):
        self.counter = counter
        self.position_strategy = position_strategy

    @classmethod
    def initialise_random_player(cls, counter):
        return cls(counter, RandomPositionSelector())

    @classmethod
    def initialise_ml_player(cls, counter):
        return cls(counter, MlPositionSelector.initialise_linear_selector())

    def update(self, series_recorder):
        self.position_strategy.update(self.counter, series_recorder)

    def choose_position(self, board):
        return self.position_strategy.choose_counter_position(board)