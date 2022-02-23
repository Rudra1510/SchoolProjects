import re
import random
import json


class GameInstance:
    def __init__(self) -> None:
        with open("Wordle/Wordle.json", "r") as f:
            JsonData = json.load(f)
            AllowedWords = JsonData["Data"]
            AllowedAnswers = JsonData["AnswerSheet"]

        GameWord = random.choice(AllowedAnswers)

        for ii in range(6):
            while True:
                UserInput = input(":::>  ").strip()[:5]
                if UserInput in AllowedWords:
                    break

            if UserInput == GameWord:
                print(
                    f":::>>>>>>    Congratulations, you've solved this wordle in {ii+1} tries.")

            Result = ''
            for LetterIn, LetterGame in zip(UserInput, GameWord):
                if LetterGame == LetterIn:
                    Result += "!"
                elif LetterIn in GameWord:
                    Result += "~"
                elif LetterIn not in GameWord:
                    Result += "-"

            print(f":::>  {Result.upper()}")

            if ii == 5:
                print(
                    f":::>>>>>    Sorry, but you lost this wordle. The word was {GameWord}")
