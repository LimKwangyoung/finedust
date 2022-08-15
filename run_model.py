from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler
import numpy as np

from model import LSTM_model

def run_model(csv_path: str, draw_option = False):
    def draw_graph(dataframe):
        dataframe['PM10'].plot()
        plt.title('PM10 for 10 years', fontsize=15)
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
    # scaler = StandardScaler()
    # scaler = MinMaxScaler()
    # scaler = MaxAbsScaler()
    scaler = RobustScaler()

    train_set_scaled = pd.DataFrame(scaler.fit_transform(train_set),
                                    columns=['PM10', 'SO2', 'CO', 'O3', 'NO2'], index=train_set.index)
    test_set_scaled = pd.DataFrame(scaler.fit_transform(test_set),
                                    columns=['PM10', 'SO2', 'CO', 'O3', 'NO2'], index=test_set.index)

    window_size = 30
    # def train_test_split_window(train_df, test_df, win_size):
    #     for i in range(1, win_size + 1):
    #         train_df[f"Scaled_{i}"] = train_df['PM10'].shift(i)
    #         test_df[f"Scaled_{i}"] = test_df['PM10'].shift(i)
    #
    #     X_train = train_df.dropna().drop(['PM10', 'SO2', 'CO', 'O3', 'NO2'], axis=1)
    #     y_train = train_df.dropna()[['PM10']]
    #     X_test = test_df.dropna().drop(['PM10', 'SO2', 'CO', 'O3', 'NO2'], axis=1)
    #     y_test = test_df.dropna()[['PM10']]
    #
    #     return X_train, y_train, X_test, y_test
    #
    # X_train, y_train, X_test, y_test = train_test_split_window(train_set_scaled, test_set_scaled, window_size)
    # X_train, y_train, X_test, y_test = X_train_df.values, y_train_df.values, X_test_df.values, y_test_df.values
    # X_train, X_test = X_train.reshape(X_train.shape[0], window_size, 1), X_test.reshape(X_test.shape[0], window_size, 1)

    def train_test_split_window(train_df, test_df, win_size):
        """
        y_train: from 2012-02-05 to 2019-12-31
        X_train: from 2012-01-01 for 30 days
        y_test: from 2020-02-06 to 2021-12-31
        X_test: from 2020-01-01 to for 30 days
        """
        X_train, y_train, X_test, y_test = [], [], [], []

        for i in range(train_df.shape[0] - win_size):
            X_train.append(np.array(train_df.iloc[i:i + win_size, 1:]))
            y_train.append(np.ravel(train_df.iloc[i + win_size:i + win_size + 1, 0]))
        for i in range(test_df.shape[0] - win_size):
            X_test.append(np.array(test_df.iloc[i:i + win_size, 1:]))
            y_test.append(np.ravel(test_df.iloc[i + win_size:i + win_size + 1, 0]))

        return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test)

    X_train, y_train, X_test, y_test = train_test_split_window(train_set_scaled, test_set_scaled, window_size)

    # main
    lstm = LSTM_model(X_train, y_train)
    y_pred = lstm.predict(X_test)

    y_test_df = test_set_scaled.iloc[window_size:, 0]
    y_pred_df = pd.DataFrame(y_pred, columns=['PM10'], index=y_test_df.index)
    ax_test = y_test_df.plot()
    y_pred_df.plot(ax=ax_test)
    plt.legend(['test', 'pred'])
    plt.show()

run_model(Path('./final.csv'))