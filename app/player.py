from app.constants import Constants

class Player:
    def __init__(self):
        self._hand = []
        self._original_showing_value = 0
        self._money = 30

    def get_money(self):
        return self._money

    def add_money(self, money):
        self._money = self._money + money
   
    def get_hand(self):
        return self._hand

# ©“®‚Å‚â‚éê‡
    def get_action(self, state = None):
        if self.get_hand_value() < 17:
            return Constants.hit
        else:
            return Constants.stay

# ‰ü—Ç”Å
    def get_hand_value(self):
        result = 0
        #ace_flag = False
        for card in self._hand:
        #    if card == 1:
        #        ace_flag = True
            if card > 10:
                num = 10
            else:
                num = card
            result = result + num
        #if(ace_flag and result <= 11):
        #    result += 10
        return result

# Å‰‚Ì‚¾‚¯‚µ‚©Œ©‚¦‚È‚¢‚æ‚¤‚É•ÏX
    def get_showing_value(self):
        showing = self._hand[0] if self._hand[0] < 10 else 10
#        showing = sum(self._hand[1:])
        self._original_showing_value = showing
        return showing

    def get_original_showing_value(self):
        return self._original_showing_value

    def hit(self, deck):
        card_value = deck.draw()
        self._hand.append(card_value)

    def stay(self):
        return True

    def reset_hand(self):
        self._hand = []
        self._money = 0

    def update(self,new_state,reward):
        pass
