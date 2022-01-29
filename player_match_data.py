import requests
import time
import datetime
import os
import json

path = './data/'

api_key_file = './opendota.key'
api_key_present = False

# Check for api key
if os.path.exists(api_key_file):
    api_key_present = True
    with open(api_key_file) as api_file:
        api_key = api_file.readline().strip()
    print("API key present")

# Check whether the specified path exists or not
if not os.path.exists(path):
    # Create a new directory because it does not exist 
    os.makedirs(path)
    print("Data directory is created!")

api_url = "https://api.opendota.com/api/"

# MaximumDavai
player_id = 87655200

# justicej
#player_id = 37571649


#
# returns player match history as dictionary and saves as a json
# 
def get_player_matches(player_id):
    filename = path+"player_"+str(player_id)+"_matches.json"
    request_url = api_url + "players/" + str(player_id) + "/matches/"
    payload = {}
    if api_key_present:
        payload.update({'api_key':api_key}) 
    return request_if_not_exists(filename
                                ,request_data
                                ,request_url=request_url
                                ,payload=payload)


#
# returns match data as dictionary and saves as json
#
def get_match(match_id):
    filename = path+"match_"+str(match_id)+".json"
    request_url = api_url+"matches/"+str(match_id)
    payload = {}
    if api_key_present:
        payload.update({'api_key':api_key}) 
    return request_if_not_exists(filename
                                ,request_data
                                ,request_url=request_url
                                ,payload=payload)


#
# requests player matches from the api
# saves the json as a file in path
def request_data(path, **kwargs):
    response = requests.get(kwargs['request_url'],params=kwargs['payload'])
    response_json = response.json()
    return response_json


#
# if the file in path exists, calls the function
# otherwise returns the file as a dictionary
# 
def request_if_not_exists(path,func,step=0,**kwargs):
    if step == 3:
        print('too many recursions returning empty dictionary')
        with open(path,"w") as json_file:
            json.dump({}, json_file)
        return {}

    if not os.path.exists(path):
        print('\t\tTimestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
        print("Fetching request",kwargs['request_url'])
        response_json = func(path,**kwargs)
        if "error" in response_json.keys():
            print(response_json)
            print("Error fetching request trying again...")
            time.sleep(1)
            return request_if_not_exists(path,func,step=step+1,**kwargs)
        else:
            print('Got match ',response_json['match_id'])
            with open(path,"w") as json_file:
                json.dump(response_json, json_file)
            return response_json
    else:
        #print("Request already on disk")
        with open(path) as json_file:
            return json.load(json_file)


player_matches = get_player_matches(player_id)
print(len(player_matches))

for match in player_matches:
    time.sleep(.01)
    get_match(match['match_id'])
