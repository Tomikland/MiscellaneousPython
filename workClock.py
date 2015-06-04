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
        if automatic != "y":
            t = int(input("Work how long? "))
        else:
            t = DEFAULT_WORK
        print("Work time!")
        wait(t)
        winsound.Beep(300,2000)

        if automatic != "y":
            t = int(input("Rest how long? "))
        else:
            t = DEFAULT_BREAK
        print("Break time!")
        wait(t)
        winsound.Beep(500,750)
        winsound.Beep(500,750)
    
main()
