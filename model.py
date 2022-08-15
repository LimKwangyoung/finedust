import keras.backend as K
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

from keras.callbacks import EarlyStopping

def LSTM_model(X_train, y_train, win_size):
    K.clear_session()
    model = Sequential()
    model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(win_size, 1)))
    # model.add(LSTM(30, activation='tanh', return_sequences=True, input_shape=(win_size, 1)))

    model.add(LSTM(32, return_sequences=False))
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='nadam')
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)

    model.fit(X_train, y_train, epochs=100, batch_size=16, verbose=1, callbacks=[early_stop])

    return model