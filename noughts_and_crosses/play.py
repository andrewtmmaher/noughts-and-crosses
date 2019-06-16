from . import game, player, recorder


def play_series(number_of_episodes, number_of_games):

    current_game = game.NoughtsAndCrosses()

    players = {
        1: player.Player.initialise_random_player(1),
        -1: player.Player.initialise_ml_player(-1)
    }

    for episode_number in range(number_of_episodes):

        print('Playing episode {}'.format(episode_number + 1))

        series_recorder = recorder.SeriesRecorder()

        for __ in range(number_of_games):
            game_recorder = recorder.GameRecorder()
            series_recorder.snapshot_game(current_game.play(players, game_recorder, debug=False))

        series_recorder.print_metrics()

        for current_player in players.values():
            if not current_player.position_strategy.CAN_BE_UPDATED:
                continue
            current_player.update(series_recorder)
            current_player.position_strategy.exploration_probability *= 0.8

        print()


if __name__ == '__main__':
    play_series(50, 100)
