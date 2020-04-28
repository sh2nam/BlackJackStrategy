import random
import yaml
import os
import black_jack.card as card


class Deck:
    def __init__(self, num_deck=1):
        self.config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config_card.yaml')),
                                Loader=yaml.FullLoader)
        self.card = card.Card

        # Create Deck
        self.deck = []
        self.__create_deck(num_deck)
        self.count = 0

    def __create_deck(self, num_deck):
        """create a deck"""
        for i in range(num_deck):
            for suit in self.config['suits']:
                for rank in self.config['ranking']:
                    self.deck.append(self.card(suit, rank))
        print('Deck created')

    def __count(self, card):
        """
        2 ~ 6: +1
        7 ~ 9: 0
        10, A: -1
        """
        if type(card.value) is list:
            self.count -= 1
        elif (card.value >= 2) and (card.value <= 6):
            self.count += 1
        elif (card.value >= 7) and (card.value <= 9):
            self.count += 0
        else:
            self.count -= 1

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.deck)
        print('Deck shuffled')

    def deal(self):
        """Grabs the first item from the deck"""
        single_card = self.deck.pop()
        self.__count(single_card)
        return single_card


if __name__ == "__main__":
    d = Deck()
    print(d.deck)
    print(d.shuffle())
    print(d.deck)

    for i in range(len(d.deck)):
        print(d.deal())
        print(d.count)