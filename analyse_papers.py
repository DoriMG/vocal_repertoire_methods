    # -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 06:30:35 2025

@author: door1
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

metadata = pd.read_csv('paper_list_v2.csv')
data = pd.read_csv('vocal_rep_review_v2.csv')

    
merged_data = pd.merge(data,metadata, left_on='Rayyan ID', right_on='key')
merged_data['Family'] = merged_data['Family'].str.strip()
## Clean data
merged_data['Package'] = merged_data['Package'].fillna(value='not specified')
merged_data['Language'] = merged_data['Language'].fillna(value='not specified')
merged_data['Language'] = merged_data['Language'].replace('not reported', 'not specified')
merged_data['Language'] = merged_data['Language'].replace('SPPS', 'SPSS')

## Merge all spellings of SASlab
merged_data['Package'] = merged_data['Package'].replace('AVISOFT-SASLab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('AvisoftSAS Lab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SAS Lab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft-SASLab', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASLab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASlab pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft-SASLab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASLab-Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASLabPro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASlab Pro', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASLab', 'Avisoft-SASLab Pro')
merged_data['Package'] = merged_data['Package'].replace('Avisoft SASLab', 'Avisoft-SASLab Pro')

# Resolve other spellings
merged_data['Package'] = merged_data['Package'].replace('PRAAT', 'Praat')
merged_data['Package'] = merged_data['Package'].replace('CANARY', 'Canary')
merged_data['Package'] = merged_data['Package'].replace('Automatic Mouse Ultrasound Detector', 'A-MUD')
merged_data['Package'] = merged_data['Package'].replace('Kay Sonagraph', 'Kay Sona-Graph')
merged_data['Package'] = merged_data['Package'].replace('not reported', 'not specified')

merged_data['n_animals'] = merged_data['Number of animals']
merged_data['n_animals'] = merged_data['n_animals'].replace('unclear', -1)
merged_data['n_animals'] = merged_data['n_animals'].replace('unknown', -1)
merged_data['n_animals'] = merged_data['n_animals'].replace('not reported', -1)

# Resolve journals
merged_data['journal'] = merged_data['journal'].str.lower()
merged_data['journal'] = merged_data['journal'].replace('zeitschrift fur tierpsychologie', 'ethology')
merged_data['journal'] = merged_data['journal'].replace('ethology : formerly zeitschrift fur tierpsychologie', 'ethology')

merged_data['journal'] = merged_data['journal'].replace('proceedings. biological sciences', 'proceedings of the royal society b')
merged_data['journal'] = merged_data['journal'].replace('proceedings of the royal society b: biological sciences', 'proceedings of the royal society b')
merged_data['journal'] = merged_data['journal'].replace('zeitschrift fur saugetierkunde', 'zeitschrift für säugetierkunde')
merged_data['journal'] = merged_data['journal'].replace('primates; journal of primatology', 'primates')
merged_data['journal'] = merged_data['journal'].replace('primates; journal of primatology', 'primates')



merged_data['n_recs_analysed'] = merged_data['Number of vocalizations (included in analysis)'].replace('not reported', -1)
merged_data['n_recs_analysed'] = merged_data['n_recs_analysed'].replace('unknown', -1)
merged_data['n_recs_analysed'] = merged_data['n_recs_analysed'].replace('unclear', -1)

merged_data['juvenile'] = merged_data['Repertoire size (hand, juvenile) - indicate how many calls of total repertoire are juvenile ']

merged_data['rep_size'] = merged_data['Repertoire size (hand, total)']
merged_data['rep_size'] = merged_data['rep_size'].replace('unclear', -1)

merged_data['juvenile'] = merged_data['juvenile'].fillna(value=0)


# Output merged data
merged_data.to_csv('merged_data.csv', index=False)  


# Output unique species for tree of life
np.savetxt('species.txt', merged_data['Species (Latin)'].unique(), fmt='%s')
np.savetxt('orders.txt', merged_data['Order'].unique(), fmt='%s')

#############################################################################
##Find the number of unique species per order

orders = merged_data['Order'].unique()
no_species = []
for order in orders:
    no_species +=[len(merged_data[merged_data['Order'] == order]['Species (Latin)'].unique())]

species_per_order = pd.DataFrame({'Order':orders,
                                  'unique_species':no_species})

species_per_order.to_csv('species_per_order.csv', index=False)  

#############################################################################
##Split out recordings locations and count

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])

all_locs = []
for i, record in merged_no_dupes.iterrows():
    rec_locs = record['Recording location']
    if isinstance(rec_locs, str):
        rec_locs = [x.strip() for x in rec_locs.split(',')]
        all_locs += rec_locs

unique_locs = Counter(all_locs).keys() # equals to list(set(words))
unique_vals = Counter(all_locs).values() # counts the elements' frequency
unique_perc = [x/219 for x in list(unique_vals)]

rec_locations = pd.DataFrame({'location':unique_locs,
                                  'number':unique_vals,
                                  'percs': unique_perc})

rec_locations.to_csv('rec_locations.csv', index=False)  

##############################################################################3

all_groups = []

for i, record in merged_no_dupes.iterrows():
    rec_locs = record['Group context']
    if isinstance(rec_locs, str):
        group = [x.strip() for x in rec_locs.split(',')]
        if len(group) == 1:
            all_groups += group
        else:
            all_groups += ['both']
            

unique_locs = Counter(all_groups).keys() # equals to list(set(words))
unique_vals = Counter(all_groups).values() # counts the elements' frequency
unique_perc = [x/len(all_groups) for x in list(unique_vals)]

rec_locations = pd.DataFrame({'context':unique_locs,
                                  'number':unique_vals,
                                  'percs': unique_perc})

rec_locations.to_csv('contexts.csv', index=False)  


## Stats on number of animals
temp = merged_data['n_animals'].values
temp = [int(x) for x in temp if isinstance(x, str)]
np.nanmedian(temp)

## Stats on number of vocs
temp = merged_data['n_recs_analysed'].values
temp = [int(x) for x in temp if isinstance(x, str)]
np.nanmedian(temp)

# Merge the entries with multiple species

# Columns with multiple entries to lists

# Output demerged per plot type