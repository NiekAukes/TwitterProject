import json
import os.path
import datetime
from typing import OrderedDict

#define data for the whole project to use
data = []

#open file and read all json objects
#this will make a list of dictionaries of all the tweets
with open(os.path.abspath('Data\\weer.json'), 'r') as json_file:
    data = [json.loads(line) for line in json_file]

def sorter(obj1):
    return datetime.datetime.strptime(obj1['created_at'], '%a %b %d %H:%M:%S %z %Y')

data.sort(key=sorter)

#simple test
if __name__ == "__main__":
    for d in data:
        print(d['created_at'])