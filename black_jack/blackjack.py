import black_jack.deck as d
import black_jack.hand as h
import black_jack.strategy as s
import yaml
import os
import random
import pandas as pd


# Play Black Jack
class Blackjack:
    def __init__(self, pool=1000, user_input=False, user_strategy='simple_table_strategy'):
        # Read config:
        self.__read_config()

        # Initiate a Deck and shuffle
        self.__open_new_deck()

        # pool size, payout ratio, payout
        self.pool = pool

        # user input - if user input is true then user directly inputs H/St/D decision
        self.user_input = user_input

        # name of the user strategy
        self.user_strategy = user_strategy

        # Game Information
        self.game_info_df = pd.DataFrame()

    def __read_config(self):
        """
        read config to play the game as setting
        """
        self.config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_blackjack.yaml')),
                                Loader=yaml.FullLoader)
        self.num_deck = self.config['num_deck']
        self.num_players = self.config['num_players']
        self.user_pos = self.config['user_position']
        self.bj_po = self.config['bj_po']

    def __open_new_deck(self):
        """
        open a new deck and shuffle when cards run out.
        """
        self.deck = d.Deck(self.num_deck)
        self.deck.shuffle()
        self.__cut_deck()

    def __cut_deck(self):
        """
        use a uniform distribution to cut the deck at a random point
        """
        n = len(self.deck.deck)
        cut = random.randint(round(n*0.8), round(n*0.9))
        self.deck.deck = self.deck.deck[:cut]

    def __initiate_hands(self, bet):
        """
        create hands for dealers and players
        """
        self.dealer_h = h.Hand()
        self.players_h = {i: h.Hand() for i in range(1, self.num_players+1)}
        self.user_h = self.players_h[self.user_pos]
        self.user_h.bet = bet
        if bet == 0:
            self.user_h.playing = False

    def __deal_card(self):
        """
        deal a single card, if no more card open a new deck
        """
        if not self.deck.deck:
            self.__open_new_deck()

        return self.deck.deal()

    def __initial_deal(self):
        """
        initial deal, go around players/dealer to hand out two cards
        """
        for i in range(2):
            # deal cards to players
            for j in range(1, self.num_players+1):
                if self.players_h[j] and self.players_h[j].playing:
                    self.players_h[j].add_card(self.__deal_card())

            # deal cards to dealer
            self.dealer_h.add_card(self.__deal_card())

    def __show_table(self, dealer_scnd_card=True):
        """
        print table information
        """
        print('Dealer: ', end=' ')
        print(self.dealer_h.get_hand_info(dealer_scnd_card))

        for j in range(1, self.num_players+1):
            if j == self.user_pos:
                print('User: ', end=' ')
            else:
                print('Player ' + str(j) + ': ', end=' ')

            if type(self.players_h[j]) == list:
                for h in self.players_h[j]:
                    print(h)
            else:
                print(self.players_h[j])

    def __hit(self, hand):
        """
        hit - add new card
        """
        hand.add_card(self.__deal_card())

    def __stand(self, hand):
        """
        stand - stop dealing
        """
        hand.playing = False

    def __double_down(self, hand):
        """
        double down - increase a bet amount and
        """
        if len(hand.hand) == 2:
            if hand.bet:
                hand.bet = hand.bet * 2
            hand.add_card(self.__deal_card())
            hand.playing = False
        else:
            self.__hit(hand)

    def __split(self, hand, user):
        """
        split - split two cards and deal again
        """
        # create two new hands
        h1 = h.Hand()
        h2 = h.Hand()
        h1.add_card(hand.hand[0])
        h2.add_card(hand.hand[1])
        h1.add_card(self.__deal_card())
        h2.add_card(self.__deal_card())

        # adjust the bet amount
        h1.bet = hand.bet
        h2.bet = hand.bet

        return [self.__make_player_decisions(h1, user)] + [self.__make_player_decisions(h2, user)]

    def __make_player_decisions(self, hand, user=False):
        """
        make decisions on hand
        """
        while hand.playing and not hand.bust and not hand.black_jack:
            if user:
                print('User Card: ' + hand.get_hand_info())
                inp = input('Enter decision (H / St / D / Sp): ')
                hand.decision = inp

            else:
                inp = s.Strategy(self.dealer_h, hand).simple_table_strategy()

            if inp == 'H':
                # if player decision is hit
                self.__hit(hand)
            elif inp == 'St':
                # if player decision is Stand
                self.__stand(hand)
            elif inp == 'D':
                # if player decision is double down
                self.__double_down(hand)
            elif inp == 'Sp':
                # if player decision is split
                if (hand.hand[0].grab_rank() == hand.hand[1].grab_rank()) and len(hand.hand) == 2:
                    return self.__split(hand, user)
                else:
                    print('Cannot Split, Re-enter')
            else:
                # wrong inputs
                print('Wrong input, Re-enter!')
        return hand

    def __deal_dealer_cards(self):
        # deal dealer cards
        while self.dealer_h.playing and not self.dealer_h.bust:
            # unless dealer bust, continue handing out cards
            if self.dealer_h.hand_value[0] <= 16:
                # deal card if hand value is less than or equal to 16
                self.dealer_h.add_card(self.__deal_card())
            else:
                # stop dealing
                self.dealer_h.playing = False

    def __fill_payoff(self):
        """
        fill in payoff and update pool
        """
        for i in range(1, self.num_players + 1):
            # go through each player and check if busted
            if type(self.players_h[i]) == list:
                for j in self.players_h[i]:
                    self.__calc_payoff(j)
            else:
                self.__calc_payoff(self.players_h[i])

    def __check_bust(self):
        """
        return True if all of players busted, this function is used to check whether dealer needs to be dealt cards
        """
        for i in range(1, self.num_players + 1):
            # go through each player and check if busted
            if type(self.players_h[i]) == list:
                for j in self.players_h[i]:
                    if not j.bust:
                        return False
            else:
                if not self.players_h[i].bust:
                    return False
        return True

    def __record_game_info(self):
        """
        keeps track of game information
        """
        if self.user_h is list:
            p_1st = self.user_h[0].hand[0].draw()
            p_2nd = self.user_h[1].hand[0].draw()
            decision = 'Sp'
            bet = self.user_h[0].bet + self.user_h[1].bet

        else:
            p_1st = self.user_h.hand[0].draw()
            p_2nd = self.user_h.hand[1].draw()
            decision = self.user_h.decision
            bet = self.user_h.bet

        d_1st = self.dealer_h.hand[0].draw()
        d_2nd = self.dealer_h.hand[1].draw()

        info = {'Player 1st Card': [p_1st], 'Player 2nd Card': [p_2nd], 'Player Decision': [decision], 'Bet': [bet],
                'Dealer 1st Card': [d_1st], 'Dealer 2nd Card': [d_2nd], 'Pool': [self.pool], 'Count': [self.count_user]}
        df = pd.DataFrame(info)
        self.game_info_df = pd.concat([self.game_info_df, df])

    def __calc_payoff(self, hand):
        """
        calculate payout ratio
        """
        # bust
        if self.user_h.bust:
            hand.payoff_ratio = -1

        # blackjack
        elif self.user_h.black_jack:
            hand.payoff_ratio = self.bj_po

        # dealer
        elif self.dealer_h.bust:
            hand.payoff_ratio = 1

        # lose
        elif self.user_h.hand_value[0] < self.dealer_h.hand_value[0]:
            hand.payoff_ratio = -1

        # push
        else:
            hand.payoff_ratio = 0

    def __update_pool(self):
        if type(self.user_h) == list:
            self.pool = self.pool + self.user_h[0].bet * self.user_h[0].payoff_ratio + \
                        self.user_h[1].bet * self.user_h[1].payoff_ratio
        else:
            self.pool = self.pool + self.user_h.bet * self.user_h.payoff_ratio

    def __play_blackjack(self, bet=5):

        # initiate hands
        self.__initiate_hands(bet)

        # deal cards
        print('Deal cards!')
        self.__initial_deal()

        # show hands on table
        self.__show_table()

        print('Players make decisions!')
        # go through each player and make decisions
        for i in range(1, self.num_players+1):
            if i == self.user_pos:
                self.count_user = self.deck.count
                self.players_h[i] = self.__make_player_decisions(self.players_h[i], True)
                self.user_h = self.players_h[i]

            else:
                self.players_h[i] = self.__make_player_decisions(self.players_h[i], False)

        # check if all players busted
        all_ply_busted = self.__check_bust()

        # start dealing dealer cards
        if not all_ply_busted:
            self.__deal_dealer_cards()

        if bet > 0:
            self.__fill_payoff()
            self.__update_pool()
            self.__record_game_info()

        self.__show_table(False)

    def main(self):
        inp = input("Enter bet amount or Q to quit: ")

        while inp != 'Q':
            self.__play_blackjack(int(inp))
            inp = input("Enter bet amount or Q to quit: ")
        print('Thank you for playing')
        print(self.game_info_df)


if __name__ == "__main__":
    bj = Blackjack()
    bj.main()