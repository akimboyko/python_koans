#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *

# Greed is a dice game where you roll up to five dice to accumulate
# points.  The following "score" function will be used calculate the
# score of a single roll of the dice.
#
# A greed roll is scored as follows:
#
# * A set of three ones is 1000 points
#
# * A set of three numbers (other than ones) is worth 100 times the
#   number. (e.g. three fives is 500 points).
#
# * A one (that is not part of a set of three) is worth 100 points.
#
# * A five (that is not part of a set of three) is worth 50 points.
#
# * Everything else is worth 0 points.
#
#
# Examples:
#
# score([1,1,1,5,1]) => 1150 points
# score([2,3,4,6,2]) => 0 points
# score([3,4,5,3,3]) => 350 points
# score([1,5,1,2,4]) => 250 points
#
# More scoring examples are given in the tests below:
#
# Your goal is to write the score method.

from collections import Counter

# my original
def score(dice):
    total = 0
    dice = Counter(dice)
    while len(dice):
        selected_index = next(filter(lambda n: dice[n] >= 3, [2, 3, 4, 5, 6]), None)
        if selected_index:
            total += selected_index * 100
            dice[selected_index] -= 3
        elif 1 in dice:
            selected_index = 1
            if dice[selected_index] >= 3:
                total += 1000
                dice[selected_index] -= 3
            else:
                total += 100
                dice[selected_index] -= 1
        elif 5 in dice:
            total += 50
            selected_index = 5
            dice[selected_index] -= 1
        #print(selected_index, dice)
        if selected_index:
            if dice[selected_index] == 0:
                del dice[selected_index]
        else:
            break
    return total

# Michael Sanchez
# def score(dice):
#     # A dict to count the dice values
#     d_dice = Counter(dice)
#     # Score 1's and 5's
#     score =   d_dice[1]//3 * 1000 \
#             + d_dice[1]%3 * 100  \
#             + d_dice[5]%3 * 50
#     # Score triplets according to their value
#     score += sum([d_dice[i]//3 * i * 100 for i in range(2,7)])
#     return score

# Rudy Sicard
# def score(dice):
#     score = 0
#     counts = Counter(dice)
#     _3_timers = set(v for v, count in counts.items() if count >= 3)
#     for v in _3_timers:
#         score += v * (1000 if v == 1 else 100)
#     for v, bonus in [(1, 100), (5, 50)]:
#         score += bonus * (counts[v] - (3 if v in _3_timers else 0))
#     return score

from collections import defaultdict, Counter

# Sergei Lebedev
# def score(dice):
#     coef1 = defaultdict(int, {1: 100, 5: 50})
#     coef3 = {1: 1000, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}
#
#     dice = Counter(dice)
#     total = 0
#     for n in range(1, 6 + 1):
#         total += coef3[n] * (dice[n] // 3)
#         total += coef1[n] * (dice[n] % 3)
#
#     return total

class AboutScoringProject(Koan):
    def test_score_of_an_empty_list_is_zero(self):
        self.assertEqual(0, score([]))

    def test_score_of_a_single_roll_of_5_is_50(self):
        self.assertEqual(50, score([5]))

    def test_score_of_a_single_roll_of_1_is_100(self):
        self.assertEqual(100, score([1]))

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores(self):
        self.assertEqual(300, score([1,5,5,1]))

    def test_score_of_single_2s_3s_4s_and_6s_are_zero(self):
        self.assertEqual(0, score([2,3,4,6]))

    def test_score_of_a_triple_1_is_1000(self):
        self.assertEqual(1000, score([1,1,1]))

    def test_score_of_other_triples_is_100x(self):
        self.assertEqual(200, score([2,2,2]))
        self.assertEqual(300, score([3,3,3]))
        self.assertEqual(400, score([4,4,4]))
        self.assertEqual(500, score([5,5,5]))
        self.assertEqual(600, score([6,6,6]))

    def test_score_of_mixed_is_sum(self):
        self.assertEqual(250, score([2,5,2,2,3]))
        self.assertEqual(550, score([5,5,5,5]))
        self.assertEqual(1150, score([1,1,1,5,1]))

    def test_ones_not_left_out(self):
        self.assertEqual(300, score([1,2,2,2]))
        self.assertEqual(350, score([1,5,2,2,2]))