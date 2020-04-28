class Hand:
    def __init__(self):
        self.hand = []
        self.hand_value = []
        self.bust = False
        self.playing = True
        self.black_jack = False
        self.bet = None
        self.decision = None
        self.payoff_ratio = None

    def __str__(self):
        return self.get_hand_info()

    def __check_black_jack(self):
        """
        checks if hand is blackjack
        """
        if len(self.hand) == 2 and self.hand_value[0] == 21:
            self.black_jack = True

    def __upd_h_value(self, c_value):
        """
        update hand value using card value
        """
        if type(c_value) != list:
            # if the received card value is not in list, make it to a list format
            c_value = [c_value]
        if not self.hand_value:
            # this is when hand_value was None
            self.hand_value = c_value
        else:
            # refer to the current hand value and add the new card value
            l = []
            for i in self.hand_value:
                for j in c_value:
                    if i + j < 22:
                        l.append(i + j)
            l = list(set(l))
            l.sort(reverse=True)
            self.hand_value = l

    def get_hand_info(self, second_card=False):
        """
        return hand information - print cards and total value of cards
        """
        hand = self.hand
        hand_val = self.hand_value

        if second_card:
            hand = [self.hand[1]]
            hand_val = [self.hand[1].grab_value()]

        l = []
        # Card information:
        for h in hand:
            l.append(h.draw())
        s = 'Hand - ' + ', '.join(l)

        # Card value:
        if self.bust:
            s2 = 'Busted'
        elif self.black_jack and not second_card:
            s2 = 'Blackjack'
        else:
            s2 = 'Value - ' + str(hand_val).strip('[]')

        return s + '; ' + s2

    def add_card(self, card):
        """
        update hand with a new card
        """
        # update hand
        self.hand.append(card)

        # update hand value
        self.__upd_h_value(card.grab_value())

        # Check black jack / Check if bust
        self.__check_black_jack()
        if not self.hand_value:
            self.bust = True


if __name__ == "__main__":
    import black_jack.card as cd
    import black_jack.deck as d

    dd = d.Deck()
    dd.shuffle()

    h = Hand()
    h.add_card(dd.deal())
    print(h)

    c = cd.Card

    c1 = c('H', '10')
    c2 = c('S', 'A')
    c3 = c('H', '10')
    c4 = c('H', '5')


    h = Hand()
    h.add_card(c1)
    print(h.get_hand_info())
    h.add_card(c2)
    print(h.get_hand_info())
    h.add_card(c3)
    print(h.get_hand_info())
    h.add_card(c4)
    print(h.get_hand_info())


