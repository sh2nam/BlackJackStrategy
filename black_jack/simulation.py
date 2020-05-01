import black_jack.blackjack as blackjack


def simulation_1(n=5, bet=5):
    """
    simulate blackjack game playing 200 times with a fixed bet size of $5 per game
    """
    game = blackjack.Blackjack(pool=1000, user_input=False, user_strategy='simple_table_strategy')
    for i in range(n):
        game.play_blackjack(bet)

    return game.game_info_df


if __name__ == "__main__":
    df = simulation_1(200, bet=20)
    df.to_csv(r'C:\temp\abc.csv')