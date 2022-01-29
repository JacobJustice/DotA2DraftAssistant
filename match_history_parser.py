import opendota
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# 87655200 steam32 account ID

client = opendota.OpenDota()
# client.get_matches('match-id')
# player = client.get_player(87655200)


# for matchid in match_ids:
#     client.get_matches(matchid)

p_id = 37571649

def make_dict_from_path(path):
    with open(path, 'r') as f:
        contents = f.readlines()
    contents = np.array(contents)[0]
    return json.loads(contents)

def parse_match(d, herostats, p_id):
    all_words = pd.DataFrame(d['all_word_counts'], index = ['word', 'count'])
    pick_bans = pd.DataFrame(d['picks_bans'])
    players = pd.DataFrame(d['players'])

    test = players[players['account_id'] == p_id]
    (x, y) = test.shape

    if x > 0:
        (x, y) = pick_bans.shape
        hero_ids_pb = np.array(pick_bans['hero_id'])
        hero_ids_all = np.array(herostats['localized_name'])
        hero_names = hero_ids_all[hero_ids_pb]
        pick_bans['hero_names'] = hero_names
        player_hero = np.array(test['hero_id'])[0]
        check = np.array(pick_bans['hero_id'] == player_hero)
        pick_bans['current_player'] = check
        return pick_bans.sort_values(by = ['team']), all_words, players
    else:
        return None

hero_stats_path = r'DotA2DraftAssistant\hero_stats.json'
hero_stats = pd.DataFrame(make_dict_from_path(hero_stats_path))

hero_id = np.array(hero_stats['id'])

for id in hero_id:
    client.get_hero_benchmarks(id)

# print(hero_stats.columns)

# match_path = r'C:\Users\nikhi\dota2\match_6402842723.json'
# match_data = make_dict_from_path(match_path)
# pb, words, players = parse_match(match_data, hero_stats, p_id)
# print(pb)
