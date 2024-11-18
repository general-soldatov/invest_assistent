from os import listdir
from os.path import isfile, join

mypath = 'stack_data'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != 'data.json']

print(onlyfiles)