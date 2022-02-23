
import re
import json
import random

Stats = {}


class WordleAssitant():
    def __init__(self, GameWord, verbose: bool = False) -> None:
        self.BlackList = ''
        self.GreenList = ''
        self.YellowList = ''

        with open("Wordle/Wordle.json", "r") as f:
            Data = json.load(f)
            self.Guesses = Data["Guesses"]
            self.Answers = Data["Answers"]
            self.Frequency = Data["Frequency"]
            self.Probaility = Data["Probability"]

        # self.GameWord = random.choice(self.Answers) # This is what happens in the actual game: the word is selected from a specific set of words of length 2315
        self.GameWord = GameWord  # For using external gameword

        self.Guess = 'slate'
        for i in range(5):

            self.Result = self.GameInterface(self.Guess, self.GameWord)
            self.Guesses = self.DataSetShortner(
                self.Guess, self.Result, self.Guesses)
            self.Guesses = self.DataSetPrioritizer(self.Guesses)

            if verbose:
                print(f"{i},{self.Guess}:{self.Result}")
                print([self.GreenList, self.YellowList, self.BlackList])

            if self.Result == "!!!!!":
                Stats[self.GameWord] = i+1
                if verbose:
                    return print(f"{self.GameWord}: {i+1}")
                return

            elif i == 5:
                Stats[self.GameWord] = 0
                if verbose:
                    return print(f"{self.GameWord}: 0")
                return

            elif self.Guesses == []:
                Stats[self.GameWord] = 0
                if verbose:
                    return print(f"{self.GameWord}: 0")
                return

            else:
                self.Guess = self.Guesses[0]

    def GameInterface(self, CurrentGuess, CurrentGameWord):
        Result = ''
        for i, j in zip(CurrentGuess, CurrentGameWord):
            if i == j:
                Result += '!'
            elif i in CurrentGameWord:
                Result += '~'
            elif i not in CurrentGameWord:
                Result += '-'
        return Result

    def DataSetShortner(self, CurrentGuess, CurrentResult, CurrentData):
        # Defines
        GreenList = self.GreenList
        YellowList = self.YellowList
        BlackList = self.BlackList

        # Remove the current word from the data
        if CurrentGuess in CurrentData:
            CurrentData.remove(CurrentGuess)

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
        # CurrentData = list(set(CurrentData).intersection(set(self.Answers)))

        return CurrentData

    def DataSetPrioritizer(self, CurrentData):
        DataSet = {}
        # Building Probaility Database
        for Word in CurrentData:
            for letter, n in zip(Word, range(5)):
                self.Probaility[letter][n] += 1

        # Making Word Score
        for Word in CurrentData:
            LocalLetterFrequencies = 0
            LoadedLetterFrequencies = 0
            InformationQuotient = 0
            IQString = ''
            for letter, n in zip(Word, range(5)):
                if letter not in IQString:
                    IQString += letter
                    InformationQuotient += 1
                    LocalLetterFrequencies += self.Probaility[letter][n]
                    LoadedLetterFrequencies += self.Frequency[letter]

            DataSet[Word] = int(LocalLetterFrequencies *
                                LoadedLetterFrequencies*InformationQuotient)
            # DataSet[Word] = int(WordSum*LoadedLetterFrequencies)

        DataSet = sorted(DataSet.items(),
                         key=lambda kv: (kv[1], kv[0]))[::-1]
        CurrentData = [X for (X, __) in DataSet]

        return CurrentData


# with open("Wordle/Wordle.json", "r") as f:
#     Data = json.load(f)
#     Answers = Data["Answers"]

# for ans in Answers:
#     print(Answers.index(ans))
#     WordleAssitant(ans)

# # Final Score
# DataLength = len(Stats)
# DataSum = 0
# for i in Stats:
#     DataSum += Stats[i]
# print(DataSum/DataLength)

# WordleAssitant("dandy")

with open("Wordle/Wordle.json") as f:
    Data = json.load(f)

print(WordleAssitant("nothing").DataSetPrioritizer(Data["Guesses"])[::-1][:10])
