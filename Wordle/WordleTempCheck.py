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


print(Try().Check("slate", "ulcer"))
