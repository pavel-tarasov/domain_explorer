import pathlib
import random


class WordGenerator:
    def __init__(self, source_file: pathlib.Path, seed: int = None):
        random.seed(seed)
        with open(source_file, encoding="utf-8") as file:
            self.syllables = file.read().split("\n")

    def generate_word(self, n: int):
        word = ""
        for i in range(n):
            word += random.choice(self.syllables)
        return word
