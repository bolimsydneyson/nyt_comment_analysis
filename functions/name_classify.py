# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:15:25 2020

@author: bolim
"""

#        """ Classifies a given name, male/female/unclassified (M, F, U).
#        Classification as a given gender is if the possibility is over 80%.
#        If it is not over 80% of a particular gender, it is an unclassified gender"""
#        
        
import os
path = 'C:/Users/bolim/Desktop/Thesis/names/'
file_names = os.listdir(path)

import pandas as pd
import re

name_df = pd.DataFrame()

for i in range(len(file_names)):
    tmp = pd.read_csv(path+file_names[i], header = None)
    tmp.columns = ['name','gender','count']
    tmp_year = re.sub('[^0-9]', '', file_names[i])
    tmp['year'] = tmp_year
    name_df = name_df.append(tmp, ignore_index = True)

# Reads in all names from birth year 1880.
# Just want most recent 100 years (want only the names of those alive)
# Make the classifier "robust"
    
name_df['year'] = name_df['year'].astype('int')
name_df = name_df[name_df['year'] >= 1918]
#
#name_df.to_csv('name.csv', index=False)

d = name_df.groupby(['name', 'gender'], as_index=False)['count'].sum()
name_per = d.reset_index().pivot('name', 'gender','count')
name_per = name_per.fillna(0)
name_per['Mpercent'] = (name_per['M'] - name_per['F']) / (name_per['M'] + name_per['F'])

new_df = name_per.reset_index()

#print(new_df.head())
# Mpercent >= 0.8 'M'
# Mpercent <= -0.8 'F'
# else = 'U'

import numpy as np

# Threshold = 80%
new_df['gender'] = np.where(new_df['Mpercent'] >= 0.8, 'M', np.where(new_df['Mpercent']<= -0.8, 'F', 'U'))

# Extract male/female/neutral names
male_names = new_df[new_df['gender'] == 'M']['name'] # (33559,)
female_names = new_df[new_df['gender'] == 'F']['name'] # (59483,)
neutral_names = new_df[new_df['gender'] == 'U']['name'] # (4792,)

#print(male_names[1000:1010])
#2880      Alayn
#2901       Alaz
#2905     Alazar
#2915      Alban
#2919     Albano
#2921     Albara
#2922    Albaraa
#2923     Albaro
#2925    Albeiro
#2926      Alben
#
#print(female_names[1000:1010])
#1740      Aeshia
#1746       Aetna
#1747        Aeva
#1748       Aevah
#1750       Aevry
#1751       Aevyn
#1753       Aeyla
#1755        Afaf
#1757       Afeni
#1758    Aferdita
#
#print(neutral_names[1000:1010])
#19801        Dah
#19822       Dahn
#19828        Dai
#19866       Dail
#19878     Dailey
#19879     Dailin
#19881      Daily
#19882     Dailyn
#19901      Daine
#20080    Dakkota

# Pickle and export
male_names = [name.lower() for name in male_names]
female_names = [name.lower() for name in female_names]
neutral_names = [name.lower() for name in neutral_names]

# Dump to picle
def dump_pickle(obj, filename):
    import pickle
    pickle.dump(obj, open(filename, 'wb'))

dump_pickle(male_names, 'male_names.pkl')
dump_pickle(female_names, 'female_names.pkl')
dump_pickle(neutral_names, 'neutral_names.pkl')