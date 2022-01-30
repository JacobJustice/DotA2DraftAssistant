import numpy as np
import pandas as pd
import os
import json
import argparse
import match_history_parser
import sys
from compute_winrate import compute_winrate
from pprint import pprint
parser = argparse.ArgumentParser()
parser.add_argument('--player', help='Steam32 Player ID')
parser.add_argument('--data', help='directory where data tables are stored')
parser.add_argument('--jsons', help='directory where jsons are stored')
args = parser.parse_args(sys.argv[1:])
player_id = int(args.player)
data_dir = args.data
jsons_path = args.jsons


print(player_id)

hero_stats_df = pd.read_csv('./hero_stats/all_hero_stats.csv')

## load validation set
validation_jsons = [f for f in os.listdir(jsons_path) if 'json' in f]

wins = []
for match_json in validation_jsons:
    with open(jsons_path+match_json) as json_file:
        pb, win = match_history_parser.parse_match(json.load(json_file), player_id)
    wins.append((match_json, pb, win))

gamma_scores = []
for gamma in range(1,600,10):
    successes = 0
    broken_matches = 0
    for match_json, pb, win in wins:
        if not isinstance(pb,pd.DataFrame):
            broken_matches+=1
        else:
            player_team = pb[pb['is_player'] == True]['isRadiant'].bool()

            # Sorts who is on players team and who isn't
            with_pb = pb[pb['isRadiant'] == player_team]
            with_pb = with_pb[with_pb['is_player'] == False]
            against_pb = pb[pb['isRadiant'] != player_team]

            with open('./hero_stats/hero_dict.json') as j_file:
                hero_id_dict = json.load(j_file)

            with_names = []
            for withp in with_pb['hero_id']:
                with_names.append(hero_id_dict[str(withp)])
        #    print(with_names)
            against_names = []
            for againstp in against_pb['hero_id']:
                against_names.append(hero_id_dict[str(againstp)])
        #    print(against_names)

            player_hero_id = np.array(pb[pb['is_player'] == True]['hero_id'])[0]
            players_hero = hero_id_dict[str(int(player_hero_id))]

            computed_wrs = compute_winrate(with_names, against_names, data_dir, gamma)
            #print(computed_wrs.iloc[0:5])
            #print("Hero picked:",players_hero,computed_wrs[players_hero])
            #print("Did we predict correctly?", computed_wrs[players_hero] >= .5, win)
            if (computed_wrs[players_hero] >= .5) == win:
                successes += 1
    gamma_scores.append((gamma, successes/(len(wins)-broken_matches)))
with open("gamma_scores.txt", "w") as output:
    output.write(str(gamma_scores))

