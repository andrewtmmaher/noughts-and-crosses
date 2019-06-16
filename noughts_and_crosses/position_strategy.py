import random
import numpy as np
from sklearn import linear_model, preprocessing


class PositionStrategy(object):

    CAN_BE_UPDATED = False

    def __init__(self, *args, **kwargs):
        pass

    def choose_counter_position(self, game):
        pass


class RandomPositionStrategy(PositionStrategy):

    def choose_counter_position(self, game):
        return random.randint(0, 8)


class MlPositionStrategy(PositionStrategy):

    CAN_BE_UPDATED = True

    def __init__(self, exploration_probability, position_models):
        self.exploration_probability = exploration_probability
        self.position_models = position_models

    @classmethod
    def initialise_linear_selector(cls):
        return cls(
            1.0,
            {position: initialise_linear_model() for position in range(9)}
        )

    def update(self, player_idx, series_recorder):
        for position_model_idx in range(9):
            boards = series_recorder.extract_boards(player_idx, position_model_idx)

            if boards.size == 0:
                continue

            features = create_features(boards)
            labels = series_recorder.extract_labels(player_idx, position_model_idx)
            weights = series_recorder.extract_weights(player_idx, position_model_idx)

            self.position_models[position_model_idx].partial_fit(
                features, labels, sample_weight=weights)

        print('Updated position models')

    def choose_counter_position(self, board):
        if random.random() < self.exploration_probability:
            return random.randint(0, 8)

        best_position = None
        max_probability = 0
        features = create_features(np.array(board).reshape(1, -1))
        for position, model in self.position_models.items():
            if board[position] != 0:
                continue
            probability = model.predict_proba(features)[0][1]
            if probability >= max_probability:
                max_probability = probability
                best_position = position

        return best_position


def initialise_linear_model():
    lm = linear_model.SGDClassifier(loss='log')
    lm.partial_fit(
        np.concatenate([
            create_features(np.array([0] * 9).reshape(1, -1)),
            create_features(np.array([0] * 9).reshape(1, -1))
        ]),
        np.array([1, -1]),
        np.array([1, -1])
    )

    return lm


pairwise_featurer = preprocessing.PolynomialFeatures(include_bias=False)


def create_features(board):
    return pairwise_featurer.fit_transform(board)