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
path = '/raw_names/' # All names used are uploaded in data > raw > names
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
# Limit ages from 18-65 (NYT Readers)
name_df = name_df[(name_df['year'] >= 1955) & (name_df['year'] <= 2002)]

d = name_df.groupby(['name', 'gender'], as_index=False)['count'].sum()
name_per = d.reset_index().pivot('name', 'gender','count')
name_per = name_per.fillna(0)


# male_count - female_count / total => if male_count = female_count, then it is 0.
# If completely male, it is 1. Complete female is -1.
# If 80% male, rate is 0.6; 80% female, rate is -0.6
name_per['Mpercent'] = (name_per['M'] - name_per['F']) / (name_per['M'] + name_per['F'])
new_df = name_per.reset_index()

# Threshold = 80%
import numpy as np
new_df['gender'] = np.where(new_df['Mpercent'] >= 0.6, 'M', np.where(new_df['Mpercent']<= -0.6, 'F', 'U'))

### Extract male/female/neutral names
male_names = new_df[new_df['gender'] == 'M']['name'] # 22625 names
female_names = new_df[new_df['gender'] == 'F']['name'] # 42091 names
neutral_names = new_df[new_df['gender'] == 'U']['name'] # 2136 names

# Lowercase it for analysis
male_names = [name.lower() for name in male_names]
female_names = [name.lower() for name in female_names]
neutral_names = [name.lower() for name in neutral_names]

# Dump to picle; pickled data available at github > data > output
def dump_pickle(obj, filename):
    import pickle
    pickle.dump(obj, open(filename, 'wb'))

dump_pickle(male_names, 'male_names.pkl')
dump_pickle(female_names, 'female_names.pkl')
dump_pickle(neutral_names, 'neutral_names.pkl')

# Some examples of the names are of below
#print(male_names[2000:2010])
#['benjaman', 'benjamen', 'benjamim', 'benjamin', 'benjamine', 'benjamon', 'benjamyn', 'benje', 'benjemin', 'benjerman']
#print(female_names[2000:2010])
#['ammaarah', 'ammanda', 'ammara', 'ammarah', 'ammber', 'amme', 'ammi', 'ammie', 'ammy', 'amna']
#print(neutral_names[2000:2010])
#['torre', 'tory', 'toryn', 'toshua', 'tovia', 'toy', 'traice', 'tramaine', 'tran', 'tranell']
#'skyler' in neutral_names
#Out[22]: True
