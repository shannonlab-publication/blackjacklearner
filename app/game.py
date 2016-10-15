# -*- coding: utf-8 -*-
from app.player import Player
from app.constants import Constants
from app.netlearner import DQNLearner
from app.qlearner import Learner
import numpy as np


class Game:
    def __init__(self, num_learning_rounds, learner = None, report_every=100):
        self.p = learner #p = 学習するプレイヤー
        self.win = 0 #勝利の数
        self.loss = 0 #負けの数
        self.game = 1 #ゲームの数
        self._num_learning_rounds = num_learning_rounds #学習回数
        self._report_every = report_every #学習経過報告何ターンごとにするか

    def run(self):

        # リセット
        d, p, p2, winner = self.reset_round()
        # 状態(Q-learningにおけるS)の取得 もともとの状態では
        # p1とp2(特例あり)の手札のポイントの順列がSとなる
        state = self.get_starting_state(p,p2)

        while True:

            while True:
                state = self.get_state(p, None, p2)
                p1_action = p.get_action(state)
                if p1_action == Constants.hit:
                    p.hit(d)
                    state = self.get_state(p, None, p2)
                    p.update(self.get_state(p,p1_action,p2),0)
                if p1_action == Constants.stay:
                    break            
                if self.determine_if_bust(p):
                    winner = Constants.player2
                    break

            # ディーラーのアクション定義
            while winner == None:
                p2_action = p2.get_action(state)
                if p2_action == Constants.hit:
                    p2.hit(d)
                if p2_action == Constants.stay:
                    break

            if self.determine_if_bust(p2):
                winner = Constants.player1
            
            break

        if winner is None:
            winner = self.determine_winner(p,p2)

        if winner == Constants.player1:
            self.win += 1
            p.update(self.get_state(p,p1_action,p2),1)
        else:
            self.loss += 1
            p.update(self.get_state(p,p1_action,p2),-1)

        self.game += 1

        self.report()

        if self.game == self._num_learning_rounds:
            print("Turning off learning!")
            self.p._learning = False
            self.win = 0
            self.loss = 0

    def report(self):
        if self.game % self._num_learning_rounds == 0:
            print(str(self.game) +" : "  +str(self.win / (self.win + self.loss)))
        elif self.game % self._report_every == 0:
            print(str(self.win / (self.win + self.loss)))

    def get_state(self,player1,p1_action, player2):
        return (player1.get_hand_value(), player2.get_original_showing_value())

    def get_starting_state(self,player1, player2):
        return (player1.get_hand_value(), player2.get_showing_value())

    def get_ending_state(self,player1,p1_action, player2):
        return (player1.get_hand_value(), player2.get_hand_value())

    def determine_winner(self,player1,player2):
        if player1.get_hand_value() == 21 or (player1.get_hand_value() > player2.get_hand_value() and player1.get_hand_value() <= 21):
            return Constants.player1
        else:
            return Constants.player2

    def determine_if_bust(self,player):
        if player.get_hand_value() > 21:
            return True
        else:
            return False

    def reset_round(self):
        d = Deck()
        if self.p is None:
            self.p = Learner()
        else:
            self.p.reset_hand()

        p = self.p
        p2 = Player()

        winner = None
        p.hit(d)
        p2.hit(d)
        p.hit(d)
        p2.hit(d)

        return d, p, p2, winner

class Deck:
    def __init__(self):

        self.shuffle()

    def shuffle(self):
        cards = np.arange(1,14)
        cards = np.repeat(cards,4*3) #4 suits x 3 decks
        np.random.shuffle(cards)
        self._cards = cards.tolist()

    def draw(self):
        return self._cards.pop()