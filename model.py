from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
import keras.backend as K
from keras.callbacks import EarlyStopping
from tensorflow.python import tf2

def LSTM_model(X_train, y_train):
    K.clear_session()
    model = Sequential()
    model.add(LSTM(30, return_sequences=True, input_shape=(30, 1)))
    model.add(LSTM(42))
    model.add(Dense(1, activation='linear'))
    model.compile(loss_weights='mean_squared_error', optimizer='adam')

    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)

    model.fit(X_train, y_train, epochs=50, batch_size=20, verbose=1, callbacks=[early_stop])

    return model