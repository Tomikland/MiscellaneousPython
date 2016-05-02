'''Kills all Spotify processes after two hours, so that it doesn't keep playing all night.
Displays the time remaining to the command line.
Remixing of killVivaldi.py and workClock.py.'''
from subprocess import Popen, PIPE, check_output
from re import findall
import os
import time

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60

def ouput_time_remaining(seconds):
    minutes = 0
    hours = 0
    if (seconds // SECONDS_IN_MINUTE > 0):
        minutes = seconds // SECONDS_IN_MINUTE
        seconds %= SECONDS_IN_MINUTE
        if (minutes // MINUTES_IN_HOUR > 0):
            hours = minutes // MINUTES_IN_HOUR
            minutes %= MINUTES_IN_HOUR

    output = ""
    if (hours > 0):
        output += format(hours, ">3d") + " Hour"
        if hours > 1:
            output += "s"
        else:
            output += " "
            
    if (minutes > 0):
        output += format(minutes, ">3d") + " Minute"
        if minutes > 1:
            output += "s"
        else:
            output += " "
        
    if (seconds > 0):
        output += format(seconds, ">3d") + " Second"
        if seconds > 1:
            output += "s"
        else:
            output += " "

    #os.system("cls")
    os.system("clear")
    print("Time remaining:", output)


two_hours = 2 * MINUTES_IN_HOUR * SECONDS_IN_MINUTE
time_remaining = two_hours
ouput_time_remaining(time_remaining)
for i in range (two_hours):
    time.sleep(1)
    time_remaining -= 1
    ouput_time_remaining(time_remaining)

#p = Popen('tasklist /svc /fi "imagename eq Spotify.exe"', stdout=PIPE).stdout
#p = Popen('ps -A', stdout=PIPE).stdout
p = check_output(['ps', '-A'])
#tasklist = p.read().decode('UTF-8')
tasklist = p.decode('UTF-8')
#spotifyPids = findall('\d+', tasklist)
spotifyPids = findall('(\d+) .+ spotify', tasklist)
print(spotifyPids)

try:
    for pid in spotifyPids:
        os.kill(int(pid), 1)
except OSError:
    pass
