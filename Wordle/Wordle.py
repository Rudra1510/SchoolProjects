# %%
import re
import json
import random
import os
from IPython.display import clear_output

Stats = {}


class Solver():
    def __init__(self, GameWord) -> None:
        self.BlackList = ''
        self.GreenList = ''
        self.YellowList = ''

        with open("Wordle.json", "r") as f:
            Data = json.load(f)
            self.Guesses = Data["Guesses"]
            self.Answers = Data["Answers"]
            self.Frequency = Data["Frequency"]
            self.Probaility = Data["Probability"]

        # self.GameWord = random.choice(self.Answers)
        self.GameWord = GameWord

        self.Guess = 'slate'
        for i in range(6):

            self.Result = self.Check(self.Guess, self.GameWord)
            self.Guesses = self.Limiter(self.Guess, self.Result, self.Guesses)
            self.Guesses = self.Prioritizer(self.Guesses)

            # print(f"{i},{self.Guess}:{self.Result}")

            if self.Result == "!!!!!":
                Stats[self.GameWord] = i+1
                return
                return print(f"{self.GameWord}: {i+1}")
            elif i == 5:
                Stats[self.GameWord] = 0
                return
                return print(f"{self.GameWord}: 0")
            elif self.Guesses == []:
                Stats[self.GameWord] = 0
                return
                return print(f"{self.GameWord}: 0")
            else:
                self.Guess = self.Guesses[0]

        # To Return, GameWord and i+1

    def Check(self, CurrentGuess, CurrentGameWord):
        Result = ''

        for i, j in zip(CurrentGuess, CurrentGameWord):
            if i == j:
                Result += '!'
            elif i in CurrentGameWord:
                Result += '~'
            elif i not in CurrentGameWord:
                Result += '-'
        return Result

    def CleanLists(self, CurrentGreenList, CurrentYellowList, CurrentBlackList):
        NewBlackList = ''
        for i in CurrentBlackList:
            if i not in CurrentGreenList and i not in CurrentYellowList:
                NewBlackList += i
        CurrentBlackList = NewBlackList
        return [CurrentGreenList, CurrentYellowList, CurrentBlackList]

    def Limiter(self, CurrentGuess, CurrentResult, CurrentData):

        # Defines
        GreenList = self.GreenList
        YellowList = self.YellowList
        BlackList = self.BlackList

        # Remove the current word from the data
        if CurrentGuess in CurrentData:
            CurrentData.remove(CurrentGuess)

        # Lists Cleaning
        GreenList, YellowList, BlackList = self.CleanLists(
            GreenList, YellowList, BlackList)

        # Making re pattern and updating lists
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

        # Lists Cleaning
        GreenList, YellowList, BlackList = self.CleanLists(
            GreenList, YellowList, BlackList)

        # Shortlisting Main Database according to the blocklist
        NewData = []
        for Word in CurrentData:
            REMatch = re.match(Pattern, Word)
            ConditionStatus = len(set(Word).intersection(
                set(YellowList))) == len(YellowList)
            BlackListIntersection = len(set(Word).intersection(set(BlackList)))
            if BlackListIntersection == 0 and REMatch != None and ConditionStatus == True:
                NewData.append(Word)
        CurrentData = NewData

        # Optimizing
        CurrentData = list(set(CurrentData).intersection(set(self.Answers)))

        return CurrentData

    def Prioritizer(self, CurrentData):

        DataSet = {}

        # Building Probaility Database
        for Word in CurrentData:
            for letter, n in zip(Word, range(5)):
                self.Probaility[letter][n] += 1

        # Making Word Score
        for Word in CurrentData:
            LocalLetterFrequencies = 0
            LoadedLetterFrequencies = 0
            WordDiversity = 0
            WordDiversityString = ''
            for letter, n in zip(Word, range(5)):
                if letter not in WordDiversityString:
                    WordDiversityString += letter
                    WordDiversity += 1
                    LocalLetterFrequencies += self.Probaility[letter][n]
                    LoadedLetterFrequencies += self.Frequency[letter]

            DataSet[Word] = int(LocalLetterFrequencies *
                                LoadedLetterFrequencies*WordDiversity)
            # DataSet[Word] = int(WordSum*LoadedLetterFrequencies)

        DataSet = sorted(DataSet.items(),
                         key=lambda kv: (kv[1], kv[0]))[::-1]

        CurrentData = [X for (X, __) in DataSet]

        return CurrentData


# Solver()
with open("Wordle.json", "r") as f:
    Data = json.load(f)
    Answers = Data["Answers"]

for ans in Answers:
    print(Answers.index(ans))
    Solver(ans)

# %%
# Final Score

TrueScore = 0
NaNData = [i for i in Stats if Stats[i] != 0]
for Word in NaNData:
    TrueScore += Stats[Word]
print(f"True Score: {round(TrueScore/len(NaNData),2)} tries")


DataLength = len(Stats)
DataSum = 0
for i in Stats:
    DataSum += Stats[i]
print(f"Raw Score: {round(DataSum/DataLength,2)} tries.")

print(f"Accuracy Rate: {round((len(NaNData)/len(Stats)*100),2)}%")

# %%
