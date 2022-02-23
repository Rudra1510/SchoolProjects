import re
import json

with open("Wordle/Wordle.json", "r") as f:
    JsonData = json.load(f)
    Guesses = JsonData["Guesses"]
    AnswerSheet = JsonData["Answers"]
    LetterFrequencies = JsonData['LetterFrequencies']
    ProbabilityData = JsonData["Probability"]

BlackList = ''
GreenList = ''
YellowList = ''


def WordleSolver(CurrentGuess, CurrentResult, Guesses):
    global BlackList
    global GreenList
    global YellowList

    if CurrentGuess in Guesses:
        Guesses.remove(CurrentGuess)

    NewBlackList = ''
    for i in BlackList:
        if i not in GreenList and i not in YellowList:
            NewBlackList += i
    BlackList = NewBlackList

    # Making a Pattern for re.match from the given data
    Pattern = ''
    for i, j in zip(CurrentGuess, CurrentResult):
        if j == "!":
            Pattern += i
            if i not in GreenList:
                GreenList += i
        elif j == "~":
            Pattern += f"([^{i}])"
            if i not in YellowList:
                YellowList += i
        elif j == "-":
            Pattern += "(.)"
            if i in GreenList or i in YellowList:
                pass
            elif i not in BlackList:
                BlackList += i

    NewBlackList = ''
    for i in BlackList:
        if i not in GreenList and i not in YellowList:
            NewBlackList += i
    BlackList = NewBlackList

    # Shortlisting Main Database according to the blocklist
    NewData = []
    for Word in Guesses:

        REMatch = re.match(Pattern, Word)

        ConditionStatus = len(set(Word).intersection(
            set(YellowList))) == len(YellowList)

        if len(set(Word).intersection(set(BlackList))) == 0 and REMatch != None and ConditionStatus == True:
            NewData.append(Word)

    Guesses = NewData

    Guesses = list(set(Guesses).intersection(set(AnswerSheet)))

    ProbabilityData = {
        "a": [0, 0, 0, 0, 0],
        "b": [0, 0, 0, 0, 0],
        "c": [0, 0, 0, 0, 0],
        "d": [0, 0, 0, 0, 0],
        "e": [0, 0, 0, 0, 0],
        "f": [0, 0, 0, 0, 0],
        "g": [0, 0, 0, 0, 0],
        "h": [0, 0, 0, 0, 0],
        "i": [0, 0, 0, 0, 0],
        "j": [0, 0, 0, 0, 0],
        "k": [0, 0, 0, 0, 0],
        "l": [0, 0, 0, 0, 0],
        "m": [0, 0, 0, 0, 0],
        "n": [0, 0, 0, 0, 0],
        "o": [0, 0, 0, 0, 0],
        "p": [0, 0, 0, 0, 0],
        "q": [0, 0, 0, 0, 0],
        "r": [0, 0, 0, 0, 0],
        "s": [0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0],
        "u": [0, 0, 0, 0, 0],
        "v": [0, 0, 0, 0, 0],
        "w": [0, 0, 0, 0, 0],
        "x": [0, 0, 0, 0, 0],
        "y": [0, 0, 0, 0, 0],
        "z": [0, 0, 0, 0, 0],
    }

    WordSumData = {}

    for Word in Guesses:
        WordData = {}
        for letter, n in zip(Word, range(5)):
            ProbabilityData[letter][n] += 1

    for Word in Guesses:
        WordSum = 0
        LettersSum = 0

        WordRangeScore = 0
        WordTempString = ''

        for letter, n in zip(Word, range(5)):

            if letter not in WordTempString:
                WordTempString += letter
                WordRangeScore += 1

            WordSum += ProbabilityData[letter][n]
            LettersSum += LetterFrequencies[letter]
        WordSumData[Word] = int(WordSum*LettersSum*WordRangeScore)
        # WordSumData[Word] = int(WordSum*LettersSum)

    WordSumData = sorted(WordSumData.items(),
                         key=lambda kv: (kv[1], kv[0]))[::-1]

    Guesses = [X for (X, __) in WordSumData]

    return WordSumData


# while True:
#     Guess = input("Guess: ")
#     Res = input("Result: ")
#     P = WordleSolver(Guess, Res, Guesses)
#     for i in P[:10]:
#         print(i)
