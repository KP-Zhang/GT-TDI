import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


location_path = '/PeMS/2013/District 7/station_location/'
station_df = pd.read_csv(location_path + 'd07_text_meta_2013_11_07.txt', sep='\t')
print(station_df['Type'].describe())

sel_id_arr = np.load('sel_id_arr.npy')
print('sel_id_arr', sel_id_arr)

print(station_df.shape)
print(sel_id_arr.shape)
sel_id_df = station_df[station_df['ID'].isin(sel_id_arr)]

print('Before dropping', sel_id_df.shape)
sel_id_df = sel_id_df[~sel_id_df.duplicated(['Longitude'], keep=False) | sel_id_df['Type'].eq('ML')]
print('After dropping', sel_id_df.shape)
sel_id_df.to_csv(location_path + 'sel_id_df_drop_duplicates_loc.csv', header=True, index=False)
# sel_id_df.to_csv(location_path + 'sel_id_df.csv', header=True, index=False)
df_group = sel_id_df.groupby('Type').size()
print(df_group)
