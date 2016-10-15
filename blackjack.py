import random
import pandas as pd

RANK, SUIT = 0, 1

# デッキ(カード)を作る関数
def make_deck():
    suits = ['S', 'H', 'D', 'C']    # スート（記号）の定義
    ranks = range(1,14)             # ランク（数字）の定義
    deck = [(x,y) for x in ranks for y in suits]
    random.shuffle(deck)            # シャッフルする
    return deck

#ステップアップできれいに表示させる。 最初は str(player_hand)で。
def print_player_hand(player_hand):
    print ('プレイヤー (' , get_point(player_hand), '):    ')
    for card in player_hand:
        print('[', card[SUIT], card[RANK], ']')
    print()

def print_dealer_hand(dealer_hand, uncovered):
    if uncovered:
        print('ディーラー (', get_point(dealer_hand), '):    ')
    else:
        print('ディーラー ( ?? ):    ')
    flag = True
    for card in dealer_hand:
        if flag or uncovered:
            print('[' , card[SUIT], card[RANK], ']')
            flag = False
        else:
            print('[ * * ]')
    print()

# ポイント換算
def get_point(hand):
    result = 0
    ace_flag = False
    for card in hand:
        if card[RANK] == 1:
            ace_flag = True
        if card[RANK] >10:
            num = 10
        else:
            num = card[RANK]
        result = result + num
    if ace_flag and result <= 11:
        result += 10
    return result


# 勝敗判定, 判定結果(文字列)と計算後の持ちチップを返す
def win_lose(dealer_hand, player_hand, bet ,player_money):
    player_point=get_point(player_hand)
    dealer_point=get_point(dealer_hand)
    if player_point <= 21:
        if (player_point > dealer_point) or (dealer_point > 21) :
            if player_point==21:
                return ('<<プレイヤーの勝ち>>',player_money + int(bet*2.5))
            else:
                return ('<<プレイヤーの勝ち>>',player_money + 2*bet)
        elif player_point == dealer_point:
            return ('<<プッシュ>>',player_money + bet)
        else:
            return ('<<プレイヤーの負け>>',player_money)
    else:
        return ('<<プレイヤーの負け>>',player_money)

def player_op(deck, player_hand, op):
    doubled, ending = False, False
    if op == '1':
        print('[ プレイヤー：スタンド ]')
        doubled, ending = False, True

    elif op == '2':
        print('[ プレイヤー：ヒット ]')
        player_hand.append(deck.pop())
        print_player_hand(player_hand)
        doubled, ending = False, False
    elif op == '3':
        if len(player_hand) == 2:
            print('[プレイヤー：ダブル]')
            player_hand.append(deck.pop())
            print_player_hand(player_hand)
            doubled, ending = True, True
        else:
            print('( ダブルはできません。 )')

    if get_point(player_hand) > 21: #バスト判定
        print('[ プレイヤーはバストした！ ]')
        ending = True
    elif get_point(player_hand) == 21:
        print ('21です！')
        ending = True

    return doubled, ending

# ディーラーの思考ルーチンとカード操作
def dealer_op(deck,player_hand,dealer_hand):
    while get_point(player_hand) <= 21:
        if get_point(dealer_hand) >= 17:
            print('[ ディーラー：スタンド ]')
            break
        else:
            print('[ ディーラー：ヒット ]')
            dealer_hand.append(deck.pop())

        print_dealer_hand(dealer_hand, False)

def dealer_op_ai(deck, player_hand, dealer_hand):
    df = pd.read_csv('optimal_policy.csv', header=1, names=('s','hit','stay','optimal'))
    while get_point(dealer_hand) <= 21:
        state_str = '(' + str(get_point(dealer_hand)) \
         +', ' + str(player_hand[0][RANK] if player_hand[0][RANK] <11 else 10) + ')'
        optimal = (df[df['s']==state_str]['optimal'].values[0])
        if optimal == 'stay':
            print('[ ディーラー：スタンド ]')
            break
        elif optimal == 'hit':
            print('[ ディーラー：ヒット ]')
            dealer_hand.append(deck.pop())

        print_dealer_hand(dealer_hand, False)

def main():
    turn = 1

    # 手札
    player_hand =[]
    player_money = 100
    dealer_hand =[]

    # デッキを作る
    deck = make_deck()
    while player_money > 0:

        print('------------------')
        print('ターン', turn)
        print('所持金', player_money)
        print('------------------')

        player_hand =[]
        dealer_hand =[]

        try:
            bet = int(input('ベットする額 > '))
        except:
            print('整数で入力してください。')
            continue

        # 入力値が所持金を超えていたらやり直し
        if bet > player_money:
            print('所持金が不足しています。')
            continue
        # 入力値が0より小さかったらやり直し
        elif bet <= 0:
            print('ベットできる額は１以上です。')
            continue


        player_money -= bet

        # デッキの残りが10枚以下ならデッキを再構築&シャッフル　
        if len(deck) < 10:
            deck = make_deck()

        for i in range(2): #お互いに２枚ずつ引く
            player_hand.append(deck.pop()) # デッキからプレイヤーの手札へ
            dealer_hand.append(deck.pop()) # デッキからディーラーの手札へ

        print('- '*20)
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand, False)
        print('- '*20)

        # プレイヤーのターン
        while True:
            op = input('スタンド : 1, ヒット : 2 , ダブル : 3 > ') # 選択肢
            doubled, ending = player_op(deck, player_hand, op)
            if doubled:
                player_money -= bet
                bet += bet
            print('- '*20)
            if ending:
                break


        # ディーラーのターン
        #dealer_op(deck,player_hand,dealer_hand)
        dealer_op_ai(deck,player_hand,dealer_hand)

        print('- '*20)

        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand, True)

        # win_lose関数は判定結果のメッセージとプレイヤーの持ち金を計算して返す
        message,player_money = win_lose(dealer_hand,player_hand,bet,player_money)

        print(message)

        turn += 1

    print('ゲームオーバーです。')

if __name__ == '__main__':
    main()
