from .exceptions import PlacementException


class NoughtsAndCrosses(object):

    EMPTY_POSITION_COUNTER = 0

    COUNTER_REPRESENTATION = {
        -1: 'o',
        0: ' ',
        1: 'x'
    }

    BOARD_TEMPLATE = (
        ' {} | {} | {} '
        '\n-----------'
        '\n {} | {} | {}'
        '\n-----------'
        '\n {} | {} | {}'
    )

    WINNING_POSITIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Row-based winning conditions
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Column-based winning conditions
        (2, 4, 6), (0, 4, 8)  # Diagonal-based winning conditions
    ]

    def __init__(self, board=None):
        self.winner = None
        self.board = board or [self.__class__.EMPTY_POSITION_COUNTER] * 9

    def reset(self):
        self.__init__()

    def place_counter(self, counter, position):
        if self.board[position] != self.EMPTY_POSITION_COUNTER:
            raise PlacementException

        self.board[position] = counter

    def print_board(self):
        print(
            self.BOARD_TEMPLATE.format(
                *[self.COUNTER_REPRESENTATION[counter] for counter in self.board])
        )

    def print_winner(self):
        if self.winner is None:
            print('There was no winner')
        else:
            print('The winner was {}!'.format(
                self.__class__.COUNTER_REPRESENTATION[self.winner]))

    def is_over(self):

        for el1, el2, el3 in self.WINNING_POSITIONS:
            if self.board[el1] == self.board[el2] == self.board[el3]:
                if self.board[el1] == 0:
                    continue

                self.winner = self.board[el1]
                return True

        if 0 not in self.board:
            return True

        return False

    def play(self, players, game_recorder, debug):

        self.reset()

        current_player_idx = 1

        if debug:
            self.print_board()

        while not self.is_over():

            current_player = players[current_player_idx]
            position = current_player.choose_position(self.board)

            try:
                self.place_counter(current_player.counter, position)
            except PlacementException:
                game_recorder.record_placement_error(
                    current_player.counter, self.board, position)
                continue

            game_recorder.record_correct_placement(current_player.counter, self.board, position)

            if debug:
                self.print_board()

            current_player_idx *= -1

        game_recorder.record_winner(self.winner)
        if debug:
            self.print_winner()

        return game_recorder
