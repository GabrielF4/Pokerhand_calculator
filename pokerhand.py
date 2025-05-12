
from collections import Counter
from typing import List, Self

class PokerHand:

    RESULT = ["Loss", "Tie", "Win"]

    #Hand rating is based on the texas hold em rules: 1-10 where 1 is the highest rating which is a Royal Flush
    hand_rating: int = 0
    #Example of hand: "KH 2H 5H 6H JH"
    hand: str = ""

    def __init__(self, hand: str):
        self.hand = hand
        self.hand_rating = self.rate_hand(hand)

    #Input: Single Card (Example: "KS")
    # Returns: a integer value based on card value
    # Return values: 2, 3, 4, 5, 6, 7, 8, 9, 10 (for T), 11 (for J), 12 (for Q), 13 (for K), 14 (for A)
    def card_value(self, card: str) -> int:
        if card[0].isdigit():
            return int(card[0])
        elif card[0] == "T":
            return 10
        elif card[0] == "J":
            return 11
        elif card[0] == "Q":
            return 12
        elif card[0] == "K":
            return 13
        elif card[0] == "A":
            return 14

    #Input: string (Example: "KS 2H 5C JD TD")
    # Return: an array based of the card values (Example: [13, 2, 5, 11, 10])
    def get_card_values(self, hand: str) -> List[int]:
        arr = hand.split(" ")
        card_values = []

        for i in range(5):
            card_values.append(self.card_value(arr[i]))

        return card_values

    #Input: an array with card values (Example: [13, 2, 5, 11, 10])
    # Return: bool if values are in a sequence
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
        for key, val in counts.items():
            if val == 4:
                return True, key
        return False, 0
        
    def get_three_alike(self, values: List[int]):
        counts = Counter(values)
        for key, val in counts.items():
            if val == 3:
                return True, key
        return False, 0
        
    def get_pairs(self, values: List[int]):
        pairs = []
        counts = Counter(values)
        for key, val in counts.items():
            if val == 2:
                pairs.append(key)
        return pairs


    #Input: string (Example: "KS 2H 5C JD TD")
    #Return: integer hand rating based on the texas hold em rules
    def rate_hand(self, hand: str):

        arr = hand.split(" ")

        #Get the card values in an array
        values = sorted([self.card_value(x[0]) for x in arr])
        suits = [x[1] for x in arr]

        #Make a counter for each value
        counts = Counter(values)

        #Check for similar cards
        four_equal, four_equal_val = self.get_four_alike(counts)
        three_equal, three_equal_val = self.get_three_alike(counts)

        pairs = sorted(self.get_pairs(counts), reverse=True)
        if len(pairs) == 2:
            two_pairs = True
            pair_1_val = pairs[0]
            pair_2_val = pairs[1]
        if len(pairs) == 1:
            pair = True
            pair_val = pairs[0]

        pair = any(count == 2 for count in counts.values())
        two_pairs = Counter(counts.values())[2] == 2

        #Check for flush and straight
        flush = all(x == suits[0] for x in suits)
        straight = self.is_straight(values)
        
        #Royal Flush
        if flush and straight and values[3] == 13:
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
    
    #Input: PokerHand with the hand of the opponent
    #Return: "Loss", "Tie" or "Win" depending on who has the better hand 
    def compare_with(self, other: Self, debug = False) -> str:

        opponent_hand_rating = self.rate_hand(other.hand)

        #Comparing card ratings based on the texas hold em rules
        if debug:
            print(f"Your card rating: {self.hand_rating}\nOpponent hand rating: {opponent_hand_rating}")
        if self.hand_rating < opponent_hand_rating:
            return self.RESULT[2]
        elif self.hand_rating > opponent_hand_rating:
            return self.RESULT[0]
        else:
            #Get a value for each card and put it into an array
            your_card_values: List[int] = sorted(self.get_card_values(self.hand), reverse=True)
            opponent_card_values: List[int] = sorted(self.get_card_values(other.hand) , reverse=True)

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
    
    myhand = PokerHand("4S 6S QS 4H 5H")
    opponent_hand = PokerHand("TS 2D TH 7C 9S")

    result = myhand.compare_with(opponent_hand, debug=True)
    
    print(result)