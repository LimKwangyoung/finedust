import pandas as pd
from pathlib import Path
import numpy as np

def dataloader(input_path: Path, output_path: Path, years:tuple = tuple(range(2012, 2022))):
    def create_csv(ipt_path: Path, opt_path: Path, years: tuple):
        for year in years:
            files = list(ipt_path.glob(str(year) + '*.xlsx'))
            final_df = pd.DataFrame()

            # excel file
            if files:
                # sort ascending
                if len(files) >= 12:
                    files = files[3:] + files[:3]
                for file in files:
                    excel_file = pd.read_excel(str(file), engine='openpyxl')
                    df = excel_file.loc[excel_file['측정소명'] == '초량동', ['측정일시', 'PM10', 'SO2', 'CO', 'O3', 'NO2']]
                    df.rename(columns={'측정일시':'Date'}, inplace=True)
                    final_df = pd.concat([final_df, df])
                    print(f"{str(file)}")
            # csv file
            else:
                files = list(ipt_path.glob(str(year) + '*.csv'))
                # sort ascending
                if len(files) >= 12:
                    files = files[3:] + files[:3]
                for file in files:
                    try:
                        csv_file = pd.read_csv(str(file), encoding='cp949')
                    except UnicodeDecodeError:
                        csv_file = pd.read_csv(str(file))
                    df = csv_file.loc[csv_file['측정소명'] == '초량동', ['측정일시', 'PM10', 'SO2', 'CO', 'O3', 'NO2']]
                    df.rename(columns={'측정일시':'Date'}, inplace=True)
                    final_df = pd.concat([final_df, df])
                    print(f"{str(file)}")

            opt_path.mkdir(parents=True, exist_ok=True)
            opt_file = opt_path / (str(year) + '.csv')
            final_df.to_csv(opt_file, index=False)
            print(f"{str(year)}.csv is created.")

    def merge_by_day(ipt_path: Path, opt_path: Path, years: tuple):
        # common year
        months0 = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30,
                   '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
        # leap year
        months1 = {'01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30,
                   '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}

        opt_path.mkdir(parents=True, exist_ok=True)

        for year in years:
            csv_file = open(opt_path / (str(year) + '.csv'), mode='w')
            print('Date,PM10,SO2,CO,O3,NO2', file=csv_file)

            df = pd.read_csv(f"{ipt_path}/{str(year)}.csv")
            idx = 0

            # common year
            if df.shape[0] <= 8760:
                for month in months0:
                    for day in range(months0[month]):
                        day0 = '0' + str(day + 1) if day + 1 <= 9 else str(day + 1)
                        for i in range(24):
                            if True in np.isnan(list(df.iloc[idx + i])) or -999 in list(df.iloc[idx + i]):
                                # print(f"{str(year) + month + day0},Nan,Nan,Nan,Nan,Nan", file=csv_file)
                                break
                        else:
                            print(f"{str(year) + month + day0},{df.iloc[idx:idx + 24, 1].mean():.3f},{df.iloc[idx:idx + 24, 2].mean():.3f},"
                                  f"{df.iloc[idx:idx + 24, 3].mean():.3f},{df.iloc[idx:idx + 24, 4].mean():.3f},{df.iloc[idx:idx + 24, 5].mean():.3f}",
                                  file=csv_file)
                        idx += 24
            # leap year
            else:
                for month in months1:
                    for day in range(months1[month]):
                        day0 = '0' + str(day + 1) if day + 1 <= 9 else str(day + 1)
                        for i in range(24):
                            if True in np.isnan(list(df.iloc[idx + i])) or -999 in list(df.iloc[idx + i]):
                                # print(f"{str(year) + month + day0},Nan,Nan,Nan,Nan,Nan", file=csv_file)
                                break
                        else:
                            print(f"{str(year) + month + day0},{df.iloc[idx:idx + 24, 1].mean():.3f},{df.iloc[idx:idx + 24, 2].mean():.3f},"
                                  f"{df.iloc[idx:idx + 24, 3].mean():.3f},{df.iloc[idx:idx + 24, 4].mean():.3f},{df.iloc[idx:idx + 24, 5].mean():.3f}",
                                  file=csv_file)
                        idx += 24

            print(f"{str(year)}.csv is created.")

    def concatenate_csv(ipt_path: Path, opt_path: Path):
        final_df = pd.DataFrame()
        csv_file = list(ipt_path.glob('*.csv'))

        for csv in csv_file:
            df = pd.read_csv(csv)
            final_df = pd.concat([final_df, df])

        final_df.set_index('Date', inplace=True)

        opt_path.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(f"{opt_path}/final.csv")

    csv_data_path = Path('./csv_data')
    # create_csv(input_path, csv_data_path, years)

    new_csv_data_path = Path('./new_csv_data')
    merge_by_day(csv_data_path, new_csv_data_path, years)

    concatenate_csv(new_csv_data_path, output_path)

input_path = Path('C:\\Users\\master\\Desktop\\data')
output_path = Path('./')
years = tuple(range(2012, 2022))

dataloader(input_path, output_path, years)