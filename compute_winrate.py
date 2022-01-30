import pandas as pd

heroes_wr_with_df = pd.read_csv('./heroes_with_df.csv', index_col='localized_name')
heroes_wr_against_df = pd.read_csv('./heroes_against_df.csv', index_col='localized_name')
heroes_tally_with_df = pd.read_csv('./with_tally_df.csv', index_col='localized_name')
heroes_tally_against_df = pd.read_csv('./against_tally_df.csv', index_col='localized_name')
print(heroes_wr_with_df)

#
# can be any number of both


#
# heroes_with: list of heroes on your team that have been picked
# heroes_against: list of heroes on enemy team that have been picked
def compute_winrate(heroes_with, heroes_against):
     selected_heroes_with = heroes_wr_with_df[heroes_with]
     selected_heroes_with['sum'] = selected_heroes_with[selected_heroes_with.columns].sum(axis=1)
     selected_heroes_with = selected_heroes_with.sort_values('sum', ascending=False)
     print(selected_heroes_with)


heroes_with = ["Pudge", "Luna", "Abaddon", "Necrophos"]

compute_winrate(heroes_with, [])
