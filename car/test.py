import os
import csv
import pandas as pd
import pandas_profiling
filename = os.path.join("imports-85.data")

names = ['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration',
         'num-of-doors', 'body-style', 'drive-wheels', 'engine-location', 'wheel-base',
         'length', 'width', 'height', 'curb-weight', 'engine-type',
         'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke',
         'compression-ratio', 'horse-power', 'peak-rpm', 'city-mpg', 'highway-mpg',
         'price']

with open(filename, 'r') as raw_data:
    reader = csv.reader(raw_data)
    dataframe = pd.DataFrame(reader)

dataframe.columns = names

profile = dataframe.profile_report(title='Car Dataset')
profile.to_file(output_file='../result/car_report.html')