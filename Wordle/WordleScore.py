import json

with open("Wordle/Final.json", "r") as f:
    Data = json.load(f)

L = len(Data)
Sum = 0
for i in Data:
    Sum += Data[i]
print(Sum/L)
