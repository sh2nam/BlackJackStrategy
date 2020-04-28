import yaml
import os


class Strategy:
    def __init__(self, dealer_hand, player_hand):
        self.strat_table = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_strategy_table.yaml')),
                                     Loader=yaml.FullLoader)['StrategyTable']
        self.dealer_hand = dealer_hand
        self.player_hand = player_hand

    def __lookup_table(self, d):
        if type(d) == str:
            return d
        for i in d.keys():
            if self.dealer_hand.hand_value[0] >= i:
                return d[i]

    def simple_table_strategy(self):

        # Two same cards
        if len(self.player_hand.hand) == 2 and self.player_hand.hand[0].grab_value() == self.player_hand.hand[1].grab_value():
            tbl = self.strat_table['TwoSameCards']
            v = self.player_hand.hand[0].grab_value()
            if self.player_hand.hand[0].ace:
                v = 1
            return self.__lookup_table(tbl[v])

        # Contains Ace
        elif len(self.player_hand.hand) == 2 and (self.player_hand.hand[0].ace or self.player_hand.hand[1].ace):
            tbl = self.strat_table['Ace']
            non_ace = self.player_hand.hand[0].grab_value()
            if self.player_hand.hand[0].ace:
                non_ace = self.player_hand.hand[1].grab_value()
            return self.__lookup_table(tbl[non_ace])

        # Otherwise
        else:
            tbl = self.strat_table['Other']
            return self.__lookup_table(tbl[self.player_hand.hand_value[0]])