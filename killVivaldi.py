'''Vivaldi(.com) has a silent crash bug that forces you to manually kill every one of its processes.
This automates that task on Windows.'''
from subprocess import Popen, PIPE
from re import findall
import os

p = Popen('tasklist /svc /fi "imagename eq vivaldi.exe"', stdout=PIPE).stdout
tasklist = p.read().decode('UTF-8')
vivaldiPids = findall('\d+', tasklist)

try:
    for pid in vivaldiPids:
        os.kill(int(pid), 1)
except OSError:
    pass
