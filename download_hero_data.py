import pandas as pd
import numpy as np
import opendota
import json
import requests
import time
import os

client = opendota.OpenDota()

if not os.path.exists("./hero_stats"):
    os.mkdir("./hero_stats")

def get_all_hero_stats():
    if not os.path.exists("./hero_stats/all_hero_stats.csv"):
        hero_data = client.get_hero_stats()
        hero_data_df = pd.DataFrame(hero_data)
        hero_data_df.to_csv("./hero_stats/all_hero_stats.csv")
    return 1

def get_hero_matchups(all_hero_stats):
    url_link = "https://api.opendota.com/api/heroes/{0}/matchups"
    hero_ids = np.array(all_hero_stats['id'])

    for i, idx in enumerate(hero_ids):
        path = "./hero_stats/hero_stats_{0}.csv".format(str(idx))
        if not os.path.exists(path):
            print(url_link.format(str(idx)))
            response = requests.get(url_link.format(str(idx)))
            hero_stats_d = response.json()
            hero_stats_df = pd.DataFrame(hero_stats_d)
            hero_stats_df['winrate'] = np.array(hero_stats_df['wins'])/np.array(hero_stats_df['games_played'])
            hero_stats_df = hero_stats_df.sort_values(by = 'hero_id').reset_index()
            hero_stats_df.to_csv(path)
        if i == 59:
            time.sleep(60)
    return 1

def combine_global_hero_stats(hero_stats):
    hero_ids = np.array(hero_stats['id'])
    (x, y) = hero_stats.shape
    hero_stats['map_id'] = np.arange(0, x, 1)
    hero_names = np.array(hero_stats['localized_name'])

    winrate_grid = np.zeros((x,x))
    path = "./hero_stats/global_wr_table.csv"

    if not os.path.exists(path):
        for i, idx in enumerate(hero_ids):
            indiv_hero_stats = pd.read_csv("./hero_stats/hero_stats_{0}.csv".format(str(hero_ids[i])))
            global_winrate = np.array(indiv_hero_stats['winrate'])
            pd_indexes = np.array(indiv_hero_stats['hero_id'], dtype = int)
            pd_indexes_mapped = np.zeros(pd_indexes.size, dtype = int)
            for j in range(0, pd_indexes.size):
                pd_indexes_mapped[j] = int(hero_stats[hero_stats['id'] == pd_indexes[j]]['map_id'])
            winrate_grid[i, pd_indexes_mapped] = global_winrate

        winrate_grid = np.where(winrate_grid == 0, 0.5, winrate_grid)
        winrate_grid_df = pd.DataFrame(winrate_grid, index = hero_names, columns = hero_names)
        winrate_grid_df.to_csv(path)
    return 1



def main():
    get_all_hero_stats()
    all_hero_stats = pd.read_csv("./hero_stats/all_hero_stats.csv")
    get_hero_matchups(all_hero_stats)
    combine_global_hero_stats(all_hero_stats)

main()
