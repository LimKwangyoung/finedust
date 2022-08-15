import keras.backend as K
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from pathlib import Path

def LSTM_model(X_train, y_train):
    K.clear_session()
    model = Sequential()
    model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))

    model.add(LSTM(32, return_sequences=False))
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    # early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)

    model.fit(X_train, y_train, epochs=200, batch_size=32, verbose=1)
    # model.fit(X_train, y_train, epochs=200, batch_size=32, verbose=1, callbacks=[early_stop])

    return model