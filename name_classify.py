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

new_df['gender'] = np.where(new_df['Mpercent'] >= 0.8, 'M', np.where(new_df['Mpercent']<= -0.8, 'F', 'U'))

# Export
male_names = new_df[new_df['gender'] == 'M']['name']
female_names = new_df[new_df['gender'] == 'F']['name']
neutral_names = new_df[new_df['gender'] == 'U']['name']

male_names.to_csv('male_names.csv', index=False, header=False)
female_names.to_csv('female_names.csv', index=False, header=False)
neutral_names.to_csv('neutral_names.csv', index=False, header=False)

