import requests
import os

class Utils:
    
    """
    Basic Utility Codes
    ~~~
    """

    def Download(self, Link:str, Path:str) -> None:

        """
        File Downloader
        ~~~
        Download files from a link to a specific location - File Path.
        Based on Requests.
        """

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",}
        with open(Path,"wb") as File: 
            Content = requests.get(url=Link,headers=headers).content
            return File.write(Content)

    def CurlDownload(self,Link:str,Path:str="") -> None:
        
        """
        Curl Based File Dowloader.
        ~~~ 
        Download files to a defined path or right here with Curl.
        """

        if Path =="":
            return os.system(f"curl -O {Link}")
        else:
            return os.system(f"curl -o {Path} -O Link")

    def Size(self, Link:str) -> float:
        
        """
        Obtain File Size (MB)
        ~~~
        Obtain the file size of the provided link in MegaBytes.
        """
        return round(int(requests.head(Link).headers.get('content-length',-1))/2**20,2)

    def Notification(self, Title:str, Content:str=""):
        """
        Notifications for MacOS
        ~~~
        Create easy notifications in MacOS using this one line code.
        """
        return os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(Content, Title))


def Cipher(String:str,Mode:int=0,Shift:int=None):
    """
    """
    if Mode == 0 and Shift == None:
        print("Shift value not provided for encryption. Using default shift of [[[13]]] Bits.")
        Shift = 13
    
    Alphabets = "abcdefghijklmnopqrstuvwxyz"
    Results = ""
    CapitalLettersIndex = [i for i in range(65, 65 + 26)]
    SmallLettersIndex = [i for i in range(97, 97 + 26)]

    for Letter in String:
        if Letter.lower() in Alphabets:
            if Letter.isupper():
                if Mode == 0:
                    Results += chr(CapitalLettersIndex[(CapitalLettersIndex.index(ord(Letter)) + Shift) % 26])
                elif Mode == 1:
                    Results += chr(CapitalLettersIndex[(CapitalLettersIndex.index(ord(Letter)) - Shift) % 26])
            elif Letter.islower():
                if Mode == 0:
                    Results += chr(SmallLettersIndex[(SmallLettersIndex.index(ord(Letter)) + Shift) % 26])
                elif Mode == 1:
                    Results += chr(SmallLettersIndex[(SmallLettersIndex.index(ord(Letter)) - Shift) % 26])
        else:
            Results += Letter

    return Results


def InstagramMutualFolloweeFinder():
    import instaloader, getpass
    Data,Users = {},[]
    Client = instaloader.Instaloader()

    print("\n\n\n"+(("-"*50)+"\n")*2)
    print("\nYour Instagram Credentials. Make sure you are following all the target accounts or else the code will fail.\n")
    Client.login(input("Username:"),getpass.getpass("Password:"))
    print((("-"*50)+"\n")*2)
    print("\nEnter the Target Usernames seperated by a space in between them.\n")
    Users = input("\nTarge Usernames:").split()
    print((("-"*50)+"\n")*2)


    for i in range(len(Users)):
        Data[i] = [Followee.username for Followee in instaloader.Profile.from_username(Client.context,Users[i]).get_followees()]
    SetList = [set(Data[User]) for User in Data]

    return set.intersection(SetList)


def DiscordGifs():
    import json

    InputPath = input('JSON File Path Here\n>')
    with open(InputPath, "r") as f:
        Data = json.load(f)

    Sources = [__['src'] for __ in Data['_state']['favorites']]
    TotalLength = len(Sources)
    Sizes = [Utils().Size(__) for __ in Sources]
    TotalSize = sum(Sizes)

    print(f"There are {TotalLength} images/gifs to download and the total transaction will cost you {TotalSize} Megabytes")

    for Link in Sources:
        FileName = Link.split('/')[-1]
        print(f"Download Status {Sources.index(Link)}/{TotalLength} | {FileName}, {Utils().Size(Link)} Megabyts")
        Utils().Download(Link,"GIF/"+FileName)


def Minecord(): 
    import time
    import pyautogui as p
    
    for i in range(3): print(f"Starting in: {3-i}"); time.sleep(1)    
    Init = time.time()
    while True:
        Now = round(Init-time.time())
        print(Now)
        if Now%60==0:
            print('Chop')
            p.typewrite("m!c"); p.typewrite(["enter"])
        if Now%45==0:
            print('Fight')
            p.typewrite("m!f"); p.typewrite(["enter"])
        if Now%6==0:
            print('Mine')
            p.typewrite("m!m"); p.typewrite(["enter"])
        time.sleep(1)


def Vocabulary():
    from notion.client import NotionClient

    Word = input("Prompt: ")

    Token = 'c4dff1adadbbc50e197526b96385a060048b243f9dfb0a0652ce2d4ddc086506cdf7c720306d790837cf68d510dbabb9825edbed61386bd3be1fc46f44b003f56003723da74f938360d5fbabb3a1'
    CollectionURL = 'https://www.notion.so/therudrabarot/ddd9cee2574e447f8791787153ab966b?v=4bc63f7bbf4c403082d72ea7878569c3'
    Client = NotionClient(Token)
    Collection = Client.get_collection_view(CollectionURL)

    Words = [__.title.lower() for __ in Collection.collection.query()]

    if Word.lower() in Words:
        return False

    try:
        Base = "https://api.dictionaryapi.dev/api/v2/entries/en/" + Word.replace(' ','%20')
        Request = requests.get(Base).json()[0]
        RawMeaningList = [_Data_['definition'] for _Data_ in Request['meanings'][0]['definitions']]
        MeaningList = [_Data_['definition'] for _Data_ in Request['meanings'][0]['definitions']][:3]
        Data = {
            "Word":Word.title(),
            "RawMeaning":"; ".join(RawMeaningList),
            "Meaning":"; ".join(MeaningList),
            "Synonyms":", ".join(list(set([Synonym for _Data_ in Request['meanings'][0]['definitions'] for Synonym in _Data_['synonyms']]))[:3])
            }
    except Exception as e:
        Data = {
            "Word":Word.title(),
            "Meaning":"-",
            "Synonyms":"-"
            }

    NewRow = Collection.collection.add_row()
    NewRow.title = Data['Word']
    NewRow.Meaning = Data['Meaning']
    NewRow.Synonyms = Data['Synonyms']
    return True


class Game:
    def __init__(self) -> None:
        self.Menu()
        import random
        self.random = random

    def GetNumbers(self):
        return [self.random.randint(1,10),self.random.randint(1,10)]

    def Menu(self):
        while True:
            GameChoice = input('\nSelect the game you want to play:\n 1. Add\n 2. Sub\n 3. Mul\n[1/2/3]:-')
            if GameChoice == "1" or "add" in GameChoice.lower():
                return self.AdditionGame()
            elif GameChoice == "2" or "sub" in GameChoice.lower():
                return self.SubstractionGame()
            elif GameChoice == "3" or "mul" in GameChoice.lower():
                return self.MultiplicationGame()
            else:
                print("Incorrect Choice. Try Again.")

    def AdditionGame(self):
        while True:
            [A,B] = self.GetNumbers()

            AnswerInput = int(input(f"\nWhat is {A} + {B}:"))
            CorrectBool = AnswerInput == A + B

            if CorrectBool:
                print(f"Correct!!\n")
            elif not CorrectBool:
                print(f"No!! The correct answer is {A+B}\n")

    def SubstractionGame(self):
        while True:
            [A,B] = self.GetNumbers()
            
            AnswerInput = int(input(f"\nWhat is {A} - {B}:"))
            CorrectBool = AnswerInput == A - B

            if CorrectBool:
                print(f"Correct!!\n")
            elif not CorrectBool:
                print(f"No!! The correct answer is {A - B}\n")

    def MultiplicationGame(self):
        while True:
            [A,B] = self.GetNumbers()
            
            AnswerInput = int(input(f"\nWhat is {A} x {B}:"))
            CorrectBool = AnswerInput == A * B

            if CorrectBool:
                print(f"Correct!!\n")
            elif not CorrectBool:
                print(f"No!! The correct answer is {A*B}\n")


class CollatzConjecture:
    def __init__(self,LowerLimit:int = 1, UpperLimit:int=101) -> None:
        for x in range(LowerLimit,UpperLimit):
            y = self.CollatzFucntion(x)
            if y ==False:
                print(y,x)
                break

    def CollatzFucntion(self,x:int):
        while True:
            if x == 1:
                return True
            elif x % 2 == 1:
                x = (3*x)+ 1
            elif x%2 == 0:
                x = int(x/2)
            else:
                return False

def Beeper():
    """
    A simple beeper that beeps every one second.
    If doesn't work, try using it straight in the terminal by copy pasting the code below.
    """
    import time
    while True:
        print("\a")
        time.sleep("0.99999614")



# if __name__ == "__main__":
#     Input = input("App Drawer:\n  1. Discord Gifs Downloader\n  2. Minecord Bot\n   3. Vocabulary\n>>>")
#     if Input.isdigit():
#         AppIndex = int(Input)

#     if AppIndex == 1:
#         DiscordGifs()
#     elif AppIndex == 2:
#         Minecord()
#     elif AppIndex==3:
#         Vocabulary()

# Cipher("Rudra",0,13)


# Minecord()