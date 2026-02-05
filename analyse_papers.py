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



merged_data['n_animals'] = merged_data['Number of animals']
merged_data['n_animals'] = merged_data['n_animals'].replace('unclear', -1)
merged_data['n_animals'] = merged_data['n_animals'].replace('unknown', -1)
merged_data['n_animals'] = merged_data['n_animals'].replace('not reported', -1)

# Resolve journals
merged_data['journal'] = merged_data['journal'].str.lower()
merged_data['journal'] = merged_data['journal'].replace('zeitschrift fur tierpsychologie', 'ethology')
merged_data['journal'] = merged_data['journal'].replace('zeitschrift für tierpsychologie', 'ethology')
merged_data['journal'] = merged_data['journal'].replace('ethology : formerly zeitschrift fur tierpsychologie', 'ethology')

merged_data['journal'] = merged_data['journal'].replace('proceedings. biological sciences', 'proceedings of the royal society b')
merged_data['journal'] = merged_data['journal'].replace('proceedings of the royal society b: biological sciences', 'proceedings of the royal society b')
merged_data['journal'] = merged_data['journal'].replace('zeitschrift fur saugetierkunde', 'zeitschrift für säugetierkunde')
merged_data['journal'] = merged_data['journal'].replace('primates; journal of primatology', 'primates')
merged_data['journal'] = merged_data['journal'].replace('primates; journal of primatology', 'primates')
merged_data['journal'] = merged_data['journal'].replace('folia primatologica; international journal of primatology', 'folia primatologica')
merged_data['journal'] = merged_data['journal'].replace('naturwissenschaften', 'die naturwissenschaften')
merged_data['journal'] = merged_data['journal'].replace('zeitschrift für säugetierkunde', 'mammalian biology')
merged_data['journal'] = merged_data['journal'].replace('naturwissenschaften', 'die naturwissenschaften')
merged_data['journal'] = merged_data['journal'].replace('naturwissenschaften', 'die naturwissenschaften')


merged_data['journal'] = merged_data['journal'].str.title()


merged_data['n_recs_analysed'] = merged_data['Number of vocalizations (included in analysis)'].replace('not reported', -1)
merged_data['n_recs_analysed'] = merged_data['n_recs_analysed'].replace('unknown', -1)
merged_data['n_recs_analysed'] = merged_data['n_recs_analysed'].replace('unclear', -1)



merged_data['juvenile'] = merged_data['Repertoire size (hand, juvenile) - indicate how many calls of total repertoire are juvenile ']

merged_data['rep_size'] = merged_data['Repertoire size (hand, total)']
merged_data['rep_size'] = merged_data['rep_size'].replace('unclear', -1)

merged_data['juvenile'] = merged_data['juvenile'].fillna(value=0)
merged_data=merged_data.rename(columns={"Analysis methods (only mark when used for analysis, so e.g. don't mark UMAP if it's ONLY used for visualization)": "analysis_methods"})

# Output merged data
merged_data.to_csv('merged_data.csv', index=False)  


# Output unique species for tree of life
np.savetxt('species.txt', merged_data['Species (Latin)'].unique(), fmt='%s')
np.savetxt('orders.txt', merged_data['Order'].unique(), fmt='%s')

##############################################################################
## Count number of records with animal number reported
temp = merged_data.dropna(subset=["n_animals"])
temp['n_animals_int'] = temp['n_animals'].astype(int)
temp = temp[temp['n_animals_int']>0]
temp = temp.drop_duplicates(subset=['Rayyan ID'])


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

###########################################################################
# Number of feaatures

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])
temp_df = merged_no_dupes.dropna(subset=['analysis_methods'])
temp_df = temp_df[temp_df['Analysis based on:']!='spectrogram']
all_no_feat = []
rec = []
for i, record in temp_df.iterrows():
    no_features = record['Number of features']
    if isinstance(no_features, str):
        if no_features != 'unclear':
            no_features = [int(x.strip()) for x in no_features.split(';')]
            all_no_feat += no_features
            rec += [i]*len(no_features)
            
no_features_df = pd.DataFrame({'rec_id':rec,
                                  'features':all_no_feat})

no_features_df.to_csv('no_features.csv', index=False)     

########################################################################
## Analysis software
all_packages = []
rec = []
for i, record in temp_df.iterrows():
    no_features = record['Package']
    if isinstance(no_features, str):
        for delim in ',;':
            no_features = no_features.replace(delim, ',')
            results = no_features.split(',')
                    
        no_features = [x.strip() for x in results]
        all_packages += no_features
        rec += [i]*len(no_features)
        
packages_df = pd.DataFrame({'rec_id':rec,
                                  'package':all_packages})

## Merge all spellings of SASlab
packages_df['package'] = packages_df['package'].replace('AVISOFT-SASLab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('AvisoftSAS Lab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SAS Lab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft-SASLab', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASLab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASlab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASlab pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft-SASLab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASLab-Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASLabPro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASlab Pro', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASlab', 'Avisoft-SASLab')
packages_df['package'] = packages_df['package'].replace('Avisoft SASLab', 'Avisoft-SASLab')

# Resolve other spellings
packages_df['package'] = packages_df['package'].replace('Batsound Pro', 'BatSound')
packages_df['package'] = packages_df['package'].replace('Deepsqueak', 'DeepSqueak')
packages_df['package'] = packages_df['package'].replace('Cool Edit Pro', 'Cool Edit')
packages_df['package'] = packages_df['package'].replace('MIR Toolbox (MATLAB)', 'MATLAB')
packages_df['package'] = packages_df['package'].replace('Raven Pro', 'Raven')
packages_df['package'] = packages_df['package'].replace('SoundForge 7', 'SoundForge')
packages_df['package'] = packages_df['package'].replace('Sound Forge', 'SoundForge')
packages_df['package'] = packages_df['package'].replace('voicebox toolbox in Matlab', 'MATLAB')

packages_df['package'] = packages_df['package'].replace('PRAAT', 'Praat')
packages_df['package'] = packages_df['package'].replace('CANARY', 'Canary')
packages_df['package'] = packages_df['package'].replace('Automatic Mouse Ultrasound Detector', 'A-MUD')
packages_df['package'] = packages_df['package'].replace('Kay Sonagraph', 'Kay Sona-Graph')
packages_df['package'] = packages_df['package'].replace('not reported', 'not specified')

packages_df.to_csv('packages.csv', index=False)     

###########################################################################

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])
temp_df = merged_no_dupes.dropna(subset=['analysis_methods'])

temp_df=temp_df.reset_index()
all_no_feat = []
rec = []
analysis_df = temp_df[['Rayyan ID']].copy()
analysis_df['duration'] = 0

# syllables
analysis_df['unit_duration'] = 0
analysis_df['no_units'] = 0
analysis_df['iui'] = 0
analysis_df['unit_rate'] = 0

# frequency
analysis_df['F0'] = 0
analysis_df['PF'] = 0

# Other
analysis_df['entropy'] = 0


for i, record in temp_df.iterrows():
    feats = record['Characteristics general']
    if isinstance(feats, str):
        feat = [x.strip() for x in feats.split(',')]
        if 'duration' in feat:
            analysis_df.at[i, 'duration'] = 1
    # syllables
    feats = record['Syllables/units']
    if isinstance(feats, str):
        feat = [x.strip() for x in feats.split(',')]
        if 'unit duration'.strip() in feat:
            analysis_df.at[i, 'unit_duration'] = 1
        if 'number of units'.strip() in feat:
            analysis_df.at[i, 'no_units'] = 1
        if 'inter unit interval'.strip() in feat:
            analysis_df.at[i, 'iui'] = 1
        if 'unit range (units/s)'.strip() in feat:
            analysis_df.at[i, 'unit_rate'] = 1
    
    #Frequency
    feats = record['PRAAT measures']
    if isinstance(feats, str):
        if 'F0' in feats:
            analysis_df.at[i, 'F0'] = 1
    
    feats = record['Custom measurement of:']
    if isinstance(feats, str):
        if 'F0' in feats:
            analysis_df.at[i, 'F0'] = 1
        if 'PF' in feats:
            analysis_df.at[i, 'peak frequency'] = 1
            
    feats = record['Raven Pro measurements']
    if isinstance(feats, str):
        if 'entropy' in feats:
            analysis_df.at[i, 'entropy'] = 1

analysis_df.to_csv('features_included.csv', index=False)     

########################################################################
## Count number with multi unit

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])
temp_df = merged_no_dupes.dropna(subset=['analysis_methods'])

temp_df=temp_df[temp_df['Analysis based on:']!='spectrogram']

np.sum(temp_df['Multi-unit calls?'] == 'All') + np.sum(temp_df['Multi-unit calls?'] == 'Some')

########################################################################
## Analysis software

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])
temp_df = merged_no_dupes.dropna(subset=['analysis_methods'])

all_packages = []
rec = []
for i, record in temp_df.iterrows():
    no_features = record['Language']
    if isinstance(no_features, str):
        for delim in ',;':
            no_features = no_features.replace(delim, ',')
            results = no_features.split(',')
                    
        no_features = [x.strip() for x in results]
        all_packages += no_features
        rec += [i]*len(no_features)
        
languages_df = pd.DataFrame({'rec_id':rec,
                                  'package':all_packages})

## Merge all spellings
languages_df['package'] = languages_df['package'].replace('Statistical Analysis System', 'SAS')
languages_df['package'] = languages_df['package'].replace('Statistica', 'STATISTICA')


languages_df.to_csv('data/analysis_programs.csv', index=False)     

########################################################################
## Analysis type

merged_no_dupes = merged_data.drop_duplicates(subset=['Rayyan ID'])
temp_df = merged_no_dupes.dropna(subset=['analysis_methods'])

temp_df=temp_df.reset_index()
all_no_feat = []
rec = []
methods_df = temp_df[['Rayyan ID']].copy()

methods_df['methods'] = temp_df['analysis_methods']
methods_df['clustering'] = 0
# syllables
methods_df['DFA'] = 0
methods_df['MDS'] = 0



for i, record in temp_df.iterrows():
    feats = record['analysis_methods']

    if isinstance(feats, str):
        if 'clust' in feats:
            methods_df.at[i, 'clustering'] = 1
        if 'DFA' in feats:
            methods_df.at[i, 'DFA'] = 1
        if 'LDA' in feats:
            methods_df.at[i, 'DFA'] = 1
        if 'MDS' in feats:
            methods_df.at[i, 'MDS'] = 1
        if 'multi-dimensional scaling' in feats:
            methods_df.at[i, 'MDS'] = 1
        if 'Multidimensional Scaling' in feats:
            methods_df.at[i, 'MDS'] = 1

methods_df.to_csv('methods_included.csv', index=False) 

#################################################
## Output list of papers with DFA

dfa_data = pd.read_csv('figures/data/methods_df_manual.csv')
dfa_only = dfa_data[dfa_data['DFA'] == 1]

metadata_small = metadata[['title', 'key']]
merged_dfa = pd.merge(dfa_only,metadata_small, left_on='Rayyan ID', right_on='key')
merged_dfa.to_csv('merged_dfa.csv', index=False) 

###############################################
