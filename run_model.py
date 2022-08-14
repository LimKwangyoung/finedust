from pathlib import Path
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.python import tf2

from model import LSTM_model

def run_model(csv_path: str, draw_option = False):
    def draw_graph(dataframe):
        plt.figure(figsize=(16, 9))
        plt.plot(dataframe.index, dataframe['PM10'])
        plt.title('PM10 for 10 years', fontsize=15)
        plt.ylabel('PM10', fontsize=13)
        plt.grid(True)
        plt.show()

    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)

    if draw_option:
        draw_graph(df)

    # split
    train_set = pd.DataFrame(df.loc[:pd.Timestamp('12-31-2019'),])
    test_set = pd.DataFrame(df.loc[pd.Timestamp('01-01-2020'):,])

    # normalization
    scaler = MinMaxScaler()
    train_set_scaled = pd.DataFrame(scaler.fit_transform(train_set),
                                    columns=['PM10', 'SO2', 'CO', 'O3', 'NO2'], index=train_set.index)
    test_set_scaled = pd.DataFrame(scaler.fit_transform(test_set),
                                    columns=['PM10', 'SO2', 'CO', 'O3', 'NO2'], index=test_set.index)

    window_size = 30
    def train_test_split_window(train_df, test_df, window_size):
        for i in range(1, window_size + 1):
            train_df[f"Scaled_{i}"] = train_df['PM10'].shift(i)
            test_df[f"Scaled_{i}"] = test_df['PM10'].shift(i)

        X_train = train_df.dropna().drop(['PM10', 'SO2', 'CO', 'O3', 'NO2'], axis=1)
        y_train = train_df.dropna()[['PM10']]
        X_test = test_df.dropna().drop(['PM10', 'SO2', 'CO', 'O3', 'NO2'], axis=1)
        y_test = test_df.dropna()[['PM10']]

        return X_train.values, y_train.values, X_test.values, y_test.values

    X_train, y_train, X_test, y_test = train_test_split_window(train_set_scaled, test_set_scaled, window_size)
    X_train = X_train.reshape(X_train.shape[0], window_size, 1)
    X_test = X_test.reshape(X_test.shape[0], window_size, 1)

    model = LSTM_model(X_train, y_train)

    y_pred = model.predict(X_test)

    print(y_pred)






run_model(Path('./final.csv'))