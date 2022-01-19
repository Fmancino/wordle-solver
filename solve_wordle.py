#!/usr/bin/env python3

import random

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def all_letters_differ(word):
    return len(word) == len(set(word))

if __name__ == '__main__':
    english_words = load_words()

    five_letter_words = [ x for x in english_words if len(x) == 5 ]
    print(f"All 5 letter words: {len(five_letter_words)}")

    differ_letters = [ x for x in five_letter_words if all_letters_differ(x)]
    print(f"Different letter words: {len(differ_letters)}")

    first_guess = random.choice(differ_letters)
    print(f"first guess: {first_guess}")
