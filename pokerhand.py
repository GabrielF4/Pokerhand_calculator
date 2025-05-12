
from collections import Counter
from typing import List, Self

class PokerAnalysis:

    RANK_DICT = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }

    def is_straight(self, arr: List[int]) -> bool:
        arr = sorted(arr)
        for i in range(4):
            #Check for the sequence Ace, 2, 3, 4, 5
            if arr[0] == 2 and arr[1] == 3 and arr[2] == 4 and arr[3] == 5 and arr[4] == 14:
                return True
            #Check if values are in a row
            if arr[i] + 1 != arr[i + 1]:
                return False
        return True
    
    def get_four_alike(self, values: List[int]):
        counts = Counter(values)
        for card_rank, nr_of_cards in counts.items():
            if nr_of_cards == 4:
                return True, card_rank
        return False, 0
        
    def get_three_alike(self, values: List[int]):
        counts = Counter(values)
        for card_rank, nr_of_cards in counts.items():
            if nr_of_cards == 3:
                return True, card_rank
        return False, 0
        
    def get_pairs(self, values: List[int]):
        pairs = []
        counts = Counter(values)
        for card_rank, nr_of_cards in counts.items():
            if nr_of_cards == 2:
                pairs.append(card_rank)
        return pairs
    
    def get_card_values(self, hand: str) -> List[int]:
        cards = hand.split(" ")
        return sorted([self.RANK_DICT[x[0]] for x in cards], reverse=True)
    
    def get_card_suits(self, hand: str) -> List[str]:
        cards = hand.split(" ")
        return [x[1] for x in cards]

    def rate_hand(self, hand: str):

        #Get the card values in an array
        card_ranks: List[int] = self.get_card_values(hand)
        suits: List[str] = self.get_card_suits(hand)

        #Make a counter for each value
        counts = Counter(card_ranks)

        #Check for similar cards
        four_equal, four_equal_val = self.get_four_alike(counts)
        three_equal, three_equal_val = self.get_three_alike(counts)

        #Check pairs and values of pairs
        pairs = sorted(self.get_pairs(counts), reverse=True)
        pair, two_pairs = False, False
        if len(pairs) == 2:
            two_pairs = True
            pair_1_val = pairs[0]
            pair_2_val = pairs[1]
        if len(pairs) == 1:
            pair = True
            pair_val = pairs[0]

        #Check for flush and straight
        flush = all(x == suits[0] for x in suits)
        straight = self.is_straight(card_ranks)
        
        #Royal Flush
        if flush and straight and card_ranks[1] == 13:
            return 1
        #Straight Flush
        if flush and straight:
            return 2
        #Four alike
        if four_equal:
            return 3 - four_equal_val * 0.01
        #Full house
        if three_equal and pair:
            return 4 - three_equal_val * 0.01 - pair_val * 0.0001
        #Flush
        if flush:
            return 5
        #Straight
        if straight:
            return 6
        #Three alike
        if three_equal:
            return 7 - three_equal_val * 0.01
        #Two pair
        if two_pairs:
            return 8 - pair_1_val * 0.01 - pair_2_val * 0.0001
        #Pair
        if pair:
            return 9 - pair_val * 0.01
        #No special combination of cards
        return 10

class PokerHand:

    RESULT = ["Loss", "Tie", "Win"]

    analysis = PokerAnalysis()

    def __init__(self, hand: str):
        self.hand = hand
    
    def compare_with(self, other: Self) -> str:

        debug = True

        your_hand_rating = self.analysis.rate_hand(self.hand)
        opponent_hand_rating = self.analysis.rate_hand(other.hand)

        if debug:
            print(f"Your hand: {self.hand} - Rating = {your_hand_rating}")
            print(f"Opponents Hand: {other.hand} - Rating = {opponent_hand_rating}")

        #Comparing card ratings based on the texas hold em rules
        if your_hand_rating < opponent_hand_rating:
            return self.RESULT[2]
        elif your_hand_rating > opponent_hand_rating:
            return self.RESULT[0]
        else:
            #Get a value for each card and put it into an array
            your_card_values: List[int] = self.analysis.get_card_values(self.hand)
            opponent_card_values: List[int] = self.analysis.get_card_values(other.hand)

            if debug:
                print(f"Your card values: {your_card_values}\nOpponent hand values: {opponent_card_values}")

            #Check who has the higher cards. If cards are the same it's a draw
            for i in range(5):
                if your_card_values[i] > opponent_card_values[i]:
                    return self.RESULT[2]
                elif your_card_values[i] < opponent_card_values[i]:
                    return self.RESULT[0]

        return self.RESULT[1]

if __name__ == "__main__":
    
    myhand = PokerHand("KS TS QS JS AS")
    opponent_hand = PokerHand("TS 2D TH 7C 9S")

    result = myhand.compare_with(opponent_hand)
    
    if(result == "Win"):
        print("Your hand wins!")
    elif(result == "Loss"):
        print("Your hand loses!")
    else:
        print("It's a draw!")

    