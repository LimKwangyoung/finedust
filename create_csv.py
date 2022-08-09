import pandas as pd
from pathlib import Path

years = tuple(range(2012, 2022))

data_path = Path('C:\\Users\\master\\Desktop\\data')
output_path = Path('./csv_data')
output_path.mkdir(parents=True, exist_ok=True)

for year in years:
    files = list(data_path.glob(str(year) + '*.xlsx'))
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
            print(f'{str(file)}')
    # csv file
    else:
        files = list(data_path.glob(str(year) + '*.csv'))
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
            print(f'{str(file)}')

    output_file = output_path / (str(year) + '.csv')
    final_df.to_csv(output_file, index=False)
    print(f'{str(year)}.csv is created.')