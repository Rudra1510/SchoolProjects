import random
import json
import re
from WordleSolver import WordleSolver


with open("Wordle/Wordle.json", "r") as f:
    JsonData = json.load(f)
    Guesses = JsonData["Guesses"]
    AnswerSheet = JsonData["Answers"]
    LetterFrequencies = JsonData['LetterFrequencies']

BlackList = ''
GreenList = ''
YellowList = ''

GameWord = random.choice(AnswerSheet)

# for i in ran
