import json
import re
import random

# from Wordle.WordleTest import GameWord

Stats = {"Lost: ": 0, "1: ": 0, "2: ": 0,
                      "3: ": 0, "4: ": 0, "5: ": 0, "6: ": 0}

with open("Wordle/Wordle.json", "r") as f:
    Data = json.load(f)
    #     Guesses = Data["Data"]
    AnswerSheet = Data["Answers"]
    LetterFrequencies = Data['LetterFrequencies']

# BlackList = ''
# GreenList = ''
# YellowList = ''


# TempLenght = len(AnswerSheet)
# for __ in range(TempLenght):


class Try():

    def Check(self, GivenGuess, GivenGameWord):
        Result = ''

        for i, j in zip(GivenGuess, GivenGameWord):
            if i == j:
                Result += '!'
            elif i in GivenGameWord:
                Result += '~'
            elif i not in GivenGameWord:
                Result += '-'
        return Result

    def Run(self):
        global Stats
        self.Stats = Stats

        Stats = self.Stats

        with open("Wordle/Wordle.json", "r") as f:
            self.Data = json.load(f)
            self.Guesses = self.Data["Guesses"]
            self.AnswerSheet = self.Data["Answers"]
            self.LetterFrequencies = self.Data['LetterFrequencies']

        self.GameWord = random.choice(self.AnswerSheet)

        self.BlackList = ''
        self.GreenList = ''
        self.YellowList = ''

        Guess = 'slate'
        n = 0
        # input()
        for i in range(6):

            n += 1

            Result = self.Check(Guess, self.GameWord)

            NewPrediction = self.DataShortLister(
                Guess, Result, self.Guesses)

            if NewPrediction == []:
                Stats["Lost: "] += 1
                print(f">>>>>Lost for {self.GameWord}")
                return print(self.Stats)

            (X, y) = NewPrediction[0]

            # if X in Guesses:
            Guess = X

            print(Guess, Result, NewPrediction[0], X, self.GameWord)

            if self.GameWord == X:
                Stats[str(n)+": "] += 1
                print(f">>>>>Found {X} in {n} tries.")

            elif n == 6:
                Stats["Lost: "] += 1
                print(f">>>>>Lost for {self.GameWord}")

        return print(self.Stats)

    def DataShortLister(self, CurrentGuess, CurrentResult, Guesses):
        BlackList = self.BlackList
        GreenList = self.GreenList
        YellowList = self.YellowList

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


while True:
    Try().Run()
