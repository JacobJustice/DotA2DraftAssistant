import opendota
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

pd.options.mode.chained_assignment = None  # default='warn'

# Nikhil's 87655200 steam32 account ID

client = opendota.OpenDota()

# player = client.get_player(87655200)

# client.get_player_heroes(p_id)

p_id = 37571649

def make_dict_from_path(path):
    with open(path, 'r') as f:
        contents = f.readlines()
    contents = np.array(contents)[0]
    return json.loads(contents)

def parse_match(d, p_id):
    # Defines the dataframes that will be output 
    all_words = pd.DataFrame(d['all_word_counts'], index = ['word', 'count'])
    players = pd.DataFrame(d['players'])
    picks = players[['hero_id', 'isRadiant', 'account_id', 'patch']]

    test = players[players['account_id'] == p_id]
    
    (x, y) = test.shape

    if x > 0:
        check = picks['account_id'] == p_id
        picks['is_player'] = check
        win = d['radiant_win']
        return picks, win, all_words, players
    else:
        return None

def add_to_df(with_df, against_df, pb, win, hero_stats):
    # Defines whether the player is on the radiant or dire in this match
    player_team = pb[pb['is_player'] == True]['isRadiant'].bool()

    # Sorts who is on players team and who isn't
    with_pb = pb[pb['isRadiant'] == player_team]
    against_pb = pb[pb['isRadiant'] != player_team]

    # Maps player id to integer list between 0 and 121 after identifying what hero_id the player played. This step is neccessary as the hero_id does
    # not stay within the range of 0-121
    hero_id = np.array(pb[pb['is_player'] == True]['hero_id'])[0]
    hero_id_map = int(hero_stats[hero_stats['id'] == hero_id]['idx_map'])

    # Identifies hero_id for allies and enemies
    with_pb_ids = np.array(with_pb['hero_id'], dtype = int)
    against_pb_ids = np.array(against_pb['hero_id'], dtype = int)

    # Maps hero_id of allies and enemies to correct for the single jump in values
    with_pb_ids_map = np.zeros(5, dtype = int)
    against_pb_ids_map = np.zeros(5, dtype = int)

    for i in range(5):
        with_pb_ids_map[i] = int(hero_stats[hero_stats['id'] == with_pb_ids[i]]['idx_map'])
        against_pb_ids_map[i] = int(hero_stats[hero_stats['id'] == against_pb_ids[i]]['idx_map'])

    if win == True:
        with_df[hero_id_map, with_pb_ids_map] += 1
        against_df[hero_id_map, against_pb_ids_map] += 1
    
    return with_df, against_df
    
def get_hero_stats(hero_stats_path):
    hero_stats = pd.DataFrame(make_dict_from_path(hero_stats_path))
    (x, y) = hero_stats.shape
    hero_stats['idx_map'] = np.arange(0, x, 1)
    return hero_stats

def get_player_wr(player_wr_path):
    player_wr = make_dict_from_path(player_wr_path)
    player_wr = pd.DataFrame(player_wr)
    return player_wr

def main(match_path):
    hero_stats_path = 'hero_stats/hero_stats.json'
    hero_stats = get_hero_stats(hero_stats_path)

    #player_wr_path = r'C:\Users\nikhi\Documents\Clemson\CUHackit\2022\player_37571649_heroes.json'
    #player_wr = get_player_wr(player_wr_path)

    os.chdir(match_path)

    files = os.listdir()

    (x, y) = hero_stats.shape

    heroes_with = np.zeros((x, x))
    heroes_against = np.zeros((x, x))

    for match_history in files:
        match_data = make_dict_from_path(match_path + match_history)
        pb, win, words, players = parse_match(match_data, p_id)
        heroes_with, heroes_against = add_to_df(heroes_with, heroes_against, pb, win, hero_stats)

    heroes_with /= len(files)
    heroes_against /= len(files)

    print(np.unique(heroes_with), np.unique(heroes_against))

match_path = './data/training/'
main(match_path)
