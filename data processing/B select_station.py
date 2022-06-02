import os
import numpy as np
import pandas as pd
from bisect import bisect_left, bisect
import matplotlib.pyplot as plt


file_path_save = 'G:/Data/PeMS/2013/District 7/csv_2022/'
file_lst = []
ids_lst = []
for root, dirs, files in os.walk(file_path_save):
    for file_name in files:
        if file_name.endswith('.csv'):
            file_lst.append(file_name)

print('Number of files', len(file_lst))
for file_i in file_lst:
    print(file_i)
    station_df = pd.read_csv(file_path_save + file_i,
                             dtype={'Station_ID': int, 'Lane_Type': str,
                                    'Flow': int, 'Occupancy': float}, engine='c')
    # print(station_df['Station_ID'].unique())
    print(len(station_df['Station_ID'].unique()))
    ids_lst.append(station_df['Station_ID'].unique())

    # temp_df = station_df.loc[station_df['Station_ID'] == 774441]
    # plt.plot(temp_df['Flow'])
    # plt.show()
    # print(temp_df)
    # exit()

'''
Some stations in d07_text_meta_2013_11_07.txt do not have data!
Check if station x of id_lst_first exists in other id lists (i.e., ids_lst[1:]) using sort() + bisect_left(), 
then store stations existing in all id lists into sel_id_arr.
'''
# sel_id_lst = []
rem_id_lst = []
id_lst_first = ids_lst[0]
print('len(id_lst_first)', len(id_lst_first))
for id_x in id_lst_first:
    for id_lst in ids_lst[1:]:
        id_lst.sort()
        # if id_x does not exist in id_lst
        if bisect_left(id_lst, id_x) == bisect(id_lst, id_x):
            # print(id_x, "does not exist")
            rem_id_lst.append(id_x)
            # break
        # else:
        #     # print(id_x, "does not exist")
        #     rem_id_lst.append(id_x)
        #     # if id_x in set(sel_id_lst):
        #     #     set(sel_id_lst).remove(id_x)
        #     break
        # if bisect_left(id_lst, id_x) != bisect(id_lst, id_x):
        #     # print(id_x, "Exists")
        #     sel_id_lst.append(id_x)
        # else:
        #     # print(id_x, "does not exist")
        #     rem_id_lst.append(id_x)
        #     # if id_x in set(sel_id_lst):
        #     #     set(sel_id_lst).remove(id_x)
        #     break

print('Number of removed IDs', len(rem_id_lst))

sel_id_arr = np.unique(id_lst_first)
for id_r in set(rem_id_lst):
    if id_r in id_lst_first:
        sel_id_arr = np.delete(sel_id_arr, np.argwhere(sel_id_arr == id_r))
print('len(sel_id_arr)', len(sel_id_arr))
print(sel_id_arr)
np.save('sel_id_arr.npy', sel_id_arr)
