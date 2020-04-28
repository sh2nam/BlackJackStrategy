import yaml
import os


class Card:
    def __init__(self, suit, rank):
        self.card_config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_card.yaml')),
                                     Loader=yaml.FullLoader)
        self.suit = suit
        self.rank = rank
        self.value = self.card_config['card_val'][self.rank]
        self.ace = (self.rank == 'A')

    def __str__(self):
        return self.draw()

    def grab_suit(self):
        # return suit
        return self.suit

    def grab_rank(self):
        # return rank
        return self.rank

    def grab_value(self):
        # return value
        return self.value

    def draw(self):
        # return card
        return self.suit + self.rank


if __name__ == "__main__":
    a = Card('H', 'A')
    b = Card('S', '10')

    print(a.grab_suit())
    print(a.grab_rank())
    print(a.grab_value())
    print(a.draw())

    print(b.grab_suit())
    print(b.grab_rank())
    print(b.grab_value())
    print(b.draw())