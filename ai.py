import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# you could edit it from 0 to 100
p_transmission_value = 2

def load_data():
    column_names = ["POfTransmission", "Day", "NrOfSus", "NrOfInf", "NrOfRec"]
    raw_dataset = pd.read_csv("data.csv", names=column_names)
    dataset = raw_dataset.dropna()
    return dataset

def split_data(dataset):
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    return train_dataset, test_dataset


data = load_data()
train_data, test_data = split_data(data)

x = data[['POfTransmission', 'Day']].to_numpy()
NrOfSus = data['NrOfSus'].to_numpy()
NrOfInf = data['NrOfInf'].to_numpy()
NrOfRec = data['NrOfRec'].to_numpy()

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])

days = list(range(0, 500))
p_transmission = [p_transmission_value for _ in range(0, 500)]
new_x = np.dstack((p_transmission, days))

model.compile(optimizer='adam', loss='mse')

model.fit(x, NrOfSus, epochs=100, batch_size=32)

predict_nrOfSus = model.predict(list(new_x))

model.fit(x, NrOfInf, epochs=100, batch_size=32)

predict_nrOfInf = model.predict(list(new_x))

model.fit(x, NrOfRec, epochs=100, batch_size=32)

predict_nrOfRec = model.predict(list(new_x))

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(1, 1, 1)
ax.axis([0, 1000, 0, 600])
sus, = ax.plot(predict_nrOfSus, color="blue", label="Susceptible")
cinf, = ax.plot(predict_nrOfInf, color="red", label="Currently infected")
rec, = ax.plot(predict_nrOfRec, color="grey", label="Recovered")
ax.legend(handles=[rec, sus, cinf])
ax.set_xlabel("Time")
ax.set_ylabel("People")

plt.show()
