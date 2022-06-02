import gzip
import numpy as np
import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
import time
import datetime
import string
import os

split_index = pd.date_range('01/01/2013', '12/31/2013', freq='D').strftime('%m/%d/%Y')
file_path = '/PeMS/2013/District 7/'
file_path_save = '/PeMS/2013/District 7/csv_2022/'

index_i = 0
for root, dirs, files in os.walk(file_path):
    for file_name in files:
        if file_name.endswith('.gz'):
            # select data of first three months
            # if int(file_name.split('_')[5]) in range(1, 4, 1):
            start_time = time.time()
            print(file_name)
            with gzip.open(file_path + file_name, 'rt') as f:
                file_line = f.read()
                data_list = Series(file_line)
                # split raw data into rows by days
                print(split_index[index_i])
                raw_data = []

                for data in data_list.str.split(split_index[index_i]):
                    for i in data:
                        data_split = i.split(',')
                        raw_data.append(data_split)

                stations_data = pd.DataFrame(raw_data)
                station_df = {'Timestamp': pd.to_datetime(split_index[index_i] +
                                                          stations_data[0].values),
                              'Station_ID': stations_data[1].values,
                              'Lane_Type': stations_data[5].values,
                              'Flow': stations_data[9].values,
                              'Occupancy': stations_data[10].values,
                              'Speed': stations_data[11].values}

                station_df = pd.DataFrame(station_df, columns=['Timestamp', 'Station_ID', 'Lane_Type',
                                                               'Flow', 'Occupancy', 'Speed'])
                print('Before dropping nan', station_df.shape)
                station_df['Flow'].replace('', np.nan, inplace=True)
                station_df.dropna(subset=['Flow'], inplace=True)
                print('After dropping nan', station_df.shape)
                station_df.to_csv(file_path_save + str(split_index[index_i]).replace('/', '_') + '.csv',
                                  header=True, index=False)

                end_time = time.time()
                print(end_time - start_time)
                index_i = index_i + 1
