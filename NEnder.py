import time
import os



def Notification(Title:str, Content:str=""):
    """
    Notifications for MacOS
    ~~~
    Create easy notifications in MacOS using this one line code.
    """
    return os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(Content, Title))



while True:
    Result = os.popen("pgrep nsurlsessiond").read()

    try:
        Result = Result.strip().split()
    except Exception as E:
        print(type(E).__name__)
        time.sleep(2.5)
        pass

    print(Result)
    for i in Result:
        os.system(f"sudo kill -9 {i}")
#        Notification("Killed nsurlsessiond",f"PID:{i}")
    time.sleep(2.5)

