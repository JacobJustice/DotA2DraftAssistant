from compute_winrate import compute_winrate
import detect_heroes
import time
import argparse
import sys
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--data', help='directory where data tables are stored')
args = parser.parse_args(sys.argv[1:])
data_dir = args.data

radiant_draft, dire_draft = detect_heroes.get_heroes_in_draft()
print('\n\n\t\tDotA Draft Captain')
#print(radiant_draft,dire_draft,sep='\n')

with_heroes = []
against_heroes = []
old_with_heroes = with_heroes
old_against_heroes = against_heroes
while len(with_heroes)<4 or len(against_heroes)<5:
    radiant_draft, dire_draft = detect_heroes.get_heroes_in_draft()
    with_heroes = [x for x in radiant_draft if x != ""]
    against_heroes = [x for x in dire_draft if x != ""]

    if with_heroes != old_with_heroes or against_heroes != old_against_heroes:
        print('\n')
        pprint('Allies', with_heroes)
        pprint('Enemies', against_heroes)
        print('\nRecommended Picks:\n',compute_winrate(with_heroes, against_heroes, data_dir,10).iloc[0:5])

    time.sleep(3)
    old_with_heroes = with_heroes
    old_against_heroes = against_heroes

print('Good luck and have fun!')
