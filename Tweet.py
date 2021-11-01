import json
import os.path

#define data for the whole project to use
data = []

#open file and read all json objects
#this will make a list of dictionaries of all the tweets
with open(os.path.abspath('Data\\weer.json'), 'r') as json_file:
    data = [json.loads(line) for line in json_file]


#simple test
if __name__ == "__main__":
    print(data[0]['id'])