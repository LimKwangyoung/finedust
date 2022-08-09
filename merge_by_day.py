from pathlib import Path
import pandas as pd
import numpy as np

years = tuple(range(2012, 2022))
months0 = {'01':31, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31, '11':30, '12':31}
months1 = {'01':31, '02':29, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31, '11':30, '12':31}

output_path = Path('./new_csv_data')
output_path.mkdir(parents=True, exist_ok=True)

for year in years:
    new_csv_file = open(output_path / (str(year) + '.csv'), mode='w')
    print(f'Date,PM10,SO2,CO,O3,NO2', file=new_csv_file)

    csv_file = pd.read_csv('./csv_data/' + str(year) + '.csv')
    idx = 0

    # common year
    if csv_file.shape[0] <= 8760:
        for month in months0:
            for day in range(months0[month]):
                day0 = '0' + str(day + 1) if day + 1 <= 9 else str(day + 1)
                for i in range(24):
                    if True in np.isnan(list(csv_file.iloc[idx + i])) or -999 in list(csv_file.iloc[idx + i]):
                        break
                else:
                    print(f'{str(year) + month + day0},{csv_file.iloc[idx:idx + 24, 1].mean():.3f},{csv_file.iloc[idx:idx + 24, 2].mean():.3f},{csv_file.iloc[idx:idx + 24, 3].mean():.3f},{csv_file.iloc[idx:idx + 24, 4].mean():.3f},{csv_file.iloc[idx:idx + 24, 5].mean():.3f}', file=new_csv_file)
                idx += 24
    # leap year
    else:
        for month in months1:
            for day in range(months1[month]):
                day0 = '0' + str(day + 1) if day + 1 <= 9 else str(day + 1)
                for i in range(24):
                    if True in np.isnan(list(csv_file.iloc[idx + i])) or -999 in list(csv_file.iloc[idx + i]):
                        break
                else:
                    print(f'{str(year) + month + day0},{csv_file.iloc[idx:idx + 24, 1].mean():.3f},{csv_file.iloc[idx:idx + 24, 2].mean():.3f},{csv_file.iloc[idx:idx + 24, 3].mean():.3f},{csv_file.iloc[idx:idx + 24, 4].mean():.3f},{csv_file.iloc[idx:idx + 24, 5].mean():.3f}', file=new_csv_file)
                idx += 24

    print(f'{str(year)}.csv is created.')