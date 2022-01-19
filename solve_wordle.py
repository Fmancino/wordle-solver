#!/usr/bin/env python3

import random

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def all_letters_differ(word):
    return len(word) == len(set(word))

def first_guess(words):
    print("FIRST WORD")
    differ_letters = [ x for x in words if all_letters_differ(x)]
    print(f"    Different letter words: {len(differ_letters)}")
    w = guess(words)
    print(f"First guess is: {w}")
    return w

def guess(words):
    while True:
        guess = random.choice(words)
        print(f"    guessing: {guess}")
        answer = input("    Make a different guess? (y,N)\n    ")
        if answer != "y":
            break
    return guess

def main():
    english_words = load_words()

    five_letter_words = [ x for x in english_words if len(x) == 5 ]
    print(f"All 5 letter words: {len(five_letter_words)}")

    guess = first_guess(five_letter_words)

if __name__ == '__main__':
    main()
