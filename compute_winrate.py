import pandas as pd
import numpy as np
import match_history_parser
import argparse
import sys

pd.options.mode.chained_assignment = None


#parser = argparse.ArgumentParser()
#parser.add_argument('--player', help='Steam32 Player ID')
#parser.add_argument('--data', help='directory where data tables are stored')
#parser.add_argument('--jsons', help='directory where jsons are stored')
#args = parser.parse_args(sys.argv[1:])
#player_id = int(args.player)
#data_dir = args.data
#jsons_path = args.jsons


hero_stats = pd.read_csv('./hero_stats/all_hero_stats.csv', index_col='localized_name')
heroes_global_against = hero_stats['8_win']/hero_stats['8_pick']


#
# heroes_with: list of heroes on your team that have been picked
# heroes_against: list of heroes on enemy team that have been picked
def compute_winrate(heroes_with, heroes_against, data_dir, gamma):
    heroes_wr_with_df = pd.read_csv(data_dir+'/heroes_with_df.csv', index_col='localized_name')
    heroes_wr_against_df = pd.read_csv(data_dir+'/heroes_against_df.csv', index_col='localized_name')
    heroes_tally_with_df = pd.read_csv(data_dir+'/with_tally_df.csv', index_col='localized_name')
    heroes_tally_against_df = pd.read_csv(data_dir+'/against_tally_df.csv', index_col='localized_name')

    selected_heroes_with = heroes_wr_with_df[heroes_with]
    selected_tally_with = heroes_tally_with_df[heroes_with]
    selected_heroes_with_final = (selected_heroes_with/selected_tally_with).fillna(.5)
#    selected_heroes_with_final['nans'] = len(heroes_with) - selected_heroes_with_final.apply(np.ceil).sum(axis=1)

    selected_heroes_against = heroes_wr_against_df[heroes_against]
    selected_tally_against = heroes_wr_against_df[heroes_against]
    selected_heroes_against_global = heroes_global_against[heroes_against]
    selected_heroes_against_global = selected_heroes_against_global * gamma
    selected_heroes_against_final = (selected_heroes_against_global + selected_heroes_against) / (selected_tally_against + gamma)
#    print(selected_heroes_against_global)

#    selected_heroes_concat = pd.concat([selected_heroes_with_final, selected_heroes_against_final], axis=1)
#    selected_heroes_concat['sum'] = selected_heroes_concat[selected_heroes_concat.drop('nans',axis=1).columns].sum(axis=1)
#    selected_heroes_concat = selected_heroes_concat
#    final_df = (selected_heroes_concat['sum']/((len(heroes_with)-selected_heroes_with_final['nans'])+len(heroes_against))).sort_values(ascending=False)
#    
    selected_heroes_concat = pd.concat([selected_heroes_with_final, selected_heroes_against_final], axis=1)
    selected_heroes_concat['sum'] = selected_heroes_concat[selected_heroes_concat.columns].sum(axis=1)
    selected_heroes_concat = selected_heroes_concat
    final_df = (selected_heroes_concat['sum']/(len(heroes_with)+len(heroes_against))).sort_values(ascending=False)
    return final_df

#heroes_with = ["Pudge"
#                , "Luna"
#                , "Abaddon"
#                , "Necrophos"
#                ]
#
#heroes_against = ["Zeus"
#                , "Crystal Maiden"
#                , "Ogre Magi"
#                , "Dawnbreaker"
#                , "Slark"]

#print(compute_winrate(heroes_with, heroes_against))
