import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


location_path = 'G:/Data/PeMS/2013/District 7/station_location/'
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
# print(df_group)
exit()

id_lst = []
type_lst = []
for id_i in sel_id_arr:
    temp_df = station_df.loc[station_df['ID'] == id_i]
    # print(temp_df['Type'].values)
    id_lst.append(id_i)
    type_lst.append(temp_df['Type'].values)

for type_i in np.unique(type_lst):
    count = np.count_nonzero(np.asarray(type_lst) == type_i)
    print(type_i, count)
print(len(id_lst))
print(len(type_lst))
print(np.unique(type_lst))
exit()

file_path_save = 'G:/Data/PeMS/2013/District 7/csv_2022/'
file_lst = []
ids_lst = []
for root, dirs, files in os.walk(file_path_save):
    for file_name in files:
        if file_name.endswith('.csv'):
            file_lst.append(file_name)

print('Number of files', len(file_lst))
for file_i in file_lst[360:361]:
    print(file_i)
    station_df = pd.read_csv(file_path_save + file_i,
                             dtype={'Station_ID': int, 'Lane_Type': str,
                                    'Flow': int, 'Occupancy': float}, engine='c')
    # print(station_df['Station_ID'].unique())
    print(len(station_df['Station_ID'].unique()))
    ids_lst.append(station_df['Station_ID'].unique())

    for id_i in sel_id_arr:
        temp_df = station_df.loc[station_df['Station_ID'] == id_i]
        print('temp_df.shape', temp_df.shape)
        plt.plot(temp_df['Flow'])
        plt.title(str(id_i))
        plt.tight_layout()
        plt.show()
        # exit()
