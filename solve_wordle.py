#!/usr/bin/env python3
"""
Small program to help you solve the 'wordle' game
"""

import random
import json
from collections import Counter

class LetterColors:
    """
    Keep track of the colors of each letter
    """

    def __init__(self):
        """
        No letters to start
        """
        self.yellow = set()
        self.green = set()
        self.black = set()

    def update(self, word):
        """
        Update manually the colors after a guessed word.
        """
        for pos, letter in enumerate(word):
            if (pos, letter) in self.green:
                continue
            while True:
                ans = input(f"What color is letter '{letter}' in position '{pos + 1}'?\n"
                            "(g=green, y=yellow, b=black)\n")
                if ans == 'g':
                    self.green.add((pos, letter))
                    break
                if ans == 'y':
                    self.yellow.add((pos, letter))
                    break
                if ans == 'b':
                    if letter not in [ x for (_, x) in self.yellow.union(self.green) ]:
                        self.black.add(letter)
                    else:
                        self.yellow.add((pos, letter))
                    break
                print("Answer with (g=green, y=yellow, b=black)")
        print(f"Colors for word '{word}' updated correctly")

def load_words():
    """
    Load words from dictionary file
    """
    with open('words_alpha.txt', encoding='utf-8') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def all_letters_differ(word):
    """
    Do we have a word where all letters differ?
    """
    return len(word) == len(set(word))

def first_guess(words):
    """
    How to guess the first word
    """
    print("FIRST WORD")

    differ_letters = [ x for x in words if all_letters_differ(x)]
    print(f"    Different letter words: {len(differ_letters)}")

    letter_dist = Counter(''.join(differ_letters))
    #print(f"    Letter distribution: {letter_dist}")
    most_common = set(x for x, _ in letter_dist.most_common(9))
    least_common = set(x for x, _ in letter_dist.most_common()).difference(most_common)
    #print(f"    Least common letters: {least_common}")
    exclude_least = LetterColors()
    exclude_least.black = least_common
    keep_w = [x for x in differ_letters if keep(exclude_least, x)]

    print(f"    Different letter words with common letters: {len(keep_w)}")

    w = guess(keep_w)
    print(f"First guess is: {w}")
    return w

def guess(words):
    """
    Guess a word given a list of choices
    """
    words_copy = words.copy()
    while True:
        ret = random.choice(words_copy)
        print(f"    guessing: {ret}")
        answer = input("    Make a different guess?\n"
                       "    (y=yes, i=input, p=print, N=no)\n    ")
        if answer == "i":
            ret = input("    Insert own guess:\n    ")
            if len(ret) == 5:
                break
            print("    Wrong length of guess!!")
        elif answer == "p":
            print(f"    Choices: {words_copy}")
        elif answer == "y":
            words_copy.remove(ret)
        else:
            break
    if ret in words:
        words.remove(ret)
    return ret

def keep(colors, word):
    """
    Should we keep this word based on the colors of our current letters?
    """
    for pos, letter in colors.green:
        if word[pos] != letter:
            return False
    for pos, letter in colors.yellow:
        if word[pos] == letter:
            return False
        if letter not in word:
            return False
    for letter in colors.black:
        if letter in word:
            return False
    return True

def main():
    """
    Main entry point
    """
    english_words = load_words()

    colors = LetterColors()

    five_letter_words = [ x for x in english_words if len(x) == 5 ]
    print(f"All 5 letter words: {len(five_letter_words)}")

    words = five_letter_words
    res = first_guess(five_letter_words)
    count = 1
    stats = {}

    while True:
        colors.update(res)
        stats[count] = {"word": res, "choices": len(words) }
        words = [x for x in words if keep(colors, x)]
        if len(colors.green) == 5:
            print("Congratulations, you won!!")
            print("Stats:")
            print(json.dumps(stats, indent=4))
            break
        count += 1
        print(f"Remaining words in round {count}: {len(words)}")
        res = guess(words)

if __name__ == '__main__':
    main()
