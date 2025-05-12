This program compares two poker hands and returns which hand is higher. The input is of the form:

```PokerHand("KS 2H 5C JD TD")```
where the values are
```2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), A(ce)```
and the suits are
```S(pades), H(earts), D(iamonds), C(lubs)```

The rules to which hand wins is determined by Texas Hold Em ruleset:

```
1. Royal flush
A, K, Q, J, 10, all the same suit.

2. Straight flush
Five cards in a sequence, all in the same suit.

4. Four of a kind
All four cards of the same rank.

5. Full house
Three of a kind with a pair.

6. Flush
Any five cards of the same suit, but not in a sequence.

7. Straight
Five cards in a sequence, but not of the same suit.

8. Three of a kind
Three cards of the same rank.

9. Two pair
Two different pairs.

10. Pair
Two cards of the same rank.

11. High Card
When you haven't made any of the hands above, the highest card plays.
In the example below, the jack plays as the highest card.
```
