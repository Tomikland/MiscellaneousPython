import cv
import cv2
from docopt import docopt

def zext4(string):
    return ('0' * (4-len(string))) + string

def compile_data():
    data = dict()

    data[1996] = dict()
    data[1996]["video"] = "./clips/1996HINTS.mp4"
    data[1996]["starting case"] = 2

    data[1997] = dict()
    data[1997]["video"] = "./clips/1997HINTS.mp4"
    data[1997]["starting case"] = 44

    data[1998] = dict()
    data[1998]["video"] = "./clips/1998HINTS.mp4"
    data[1998]["starting case"] = 87

    data[1999] = dict()
    data[1999]["video"] = "./clips/1999HINTS.mp4"
    data[1999]["starting case"] = 130 

    data[2000] = dict()
    data[2000]["video"] = "./clips/2000HINTS.mp4"
    data[2000]["starting case"] = 175

    data[2001] = dict()
    data[2001]["video"] = "./clips/2001HINTS.mp4"
    data[2001]["starting case"] = 220

    data[2002] = dict()
    data[2002]["video"] = "./clips/2002HINTS.mp4"
    data[2002]["starting case"] = 264

    data[2003] = dict()
    data[2003]["video"] = "./clips/2003HINTS.mp4"
    data[2003]["starting case"] = 305

    data[2004] = dict()
    data[2004]["video"] = "./clips/2004HINTS.mp4"
    data[2004]["starting case"] = 346

    return data

def getpics(data):
    for year in range(1996,2004+1):
        cap = cv2.VideoCapture(data[year]["video"])
        # case min 1 because the hint is for last episode
        hintnum = data[year]["starting case"] - 1 
        for time in range(0, 500000, 2500): 
            cap.set(cv.CV_CAP_PROP_POS_MSEC, time)
            success, image = cap.read()
            print hintnum, time 
            if success:
                cv2.imwrite("pics/" + str(year) + "/nch "+zext4(str(hintnum))+".png", image)
                #cv2.imshow("20sec", image)
                #cv2.waitKey()
            else:
                print "broke on " + str(hintnum)
                break

            hintnum += 1

def main():
    getpics(compile_data())

if __name__ == "__main__":
    main()
