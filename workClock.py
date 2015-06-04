import time
import winsound

SECONDS_IN_MIN = 60
DEFAULT_WORK = 10
DEFAULT_BREAK = 5

def wait(minutes):
    
    print(minutes, "minutes remaining...")
    
    timestart = time.time()
    while (minutes > 0):
        if time.time() - timestart > SECONDS_IN_MIN:
            minutes -= 1
            if minutes > 0:
                print(minutes, "minutes remaining...")
            timestart = time.time()

    
def main():
    automatic = "q"
    while automatic != "y" and automatic != "n":
        automatic = input("Do you want automatic?(y/n): ")

    
    while(True):
        if automatic == "y":
            t = DEFAULT_WORK
        else:
            t = int(input("Work how long? "))
        print("Work time!")
        winsound.Beep(300,2000)
        wait(t)

        if automatic == "y":
            t = DEFAULT_BREAK
        else:
            t = int(input("Rest how long? "))
        print("Break time!")
        winsound.Beep(500,750)
        winsound.Beep(500,750)
        wait(t)
    
main()
