import os
import json
import argparse
import match_history_parser
import sys
from pprint import pprint
parser = argparse.ArgumentParser()
parser.add_argument('--player', help='Steam32 Player ID')
args = parser.parse_args(sys.argv[1:])
player_id = int(args.player)

print(player_id)


## load validation set
validation_jsons = [f for f in os.listdir('./data/validation/') if 'json' in f]

wins = []
for match_json in validation_jsons:
    with open('./data/validation/'+match_json) as json_file:
        _, win = match_history_parser.parse_match(json.load(json_file), player_id)
    wins.append((match_json,win))

#pprint(wins)
