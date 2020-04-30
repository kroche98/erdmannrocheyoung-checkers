import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

#model.add(Dense(activation = 'relu'))
np.random.seed(123)
#model to predict moves
model = Sequential()
#Load the game data (Kevin's Monte Carlo bot)
X = np.load('../generated_games/features-40k.npy')
Y = np.load('../generated_games.features-40k.npy')
samples = X.shape[0]
size = 8
input_shape = (size, size, 1)
#Put input into vectors of size 64 (since we have an 8x8 board)
X = X.reshape(samples, size, size, 1)
Y = Y.reshape(samples, size, size, 1)

#Train 90% of the data. The other 10% will be our test set
train_samples = int(0.9*samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

#
model.add(MaxPooling2D(pool_size = (2, 2)))

#Use the RELU activation function
model.add(Conv2D(filters = 48, kernel_size = (3,3), activation = 'relu', padding = 'same', input_shape = input_shape))
#Add second layer: page 136
model.summary()

#Use the sgd optimizer?
model.compile(loss = 'mean-squared-error', optimizer = 'sgd', metrics = ['accuracy'])
model.fit(X_train, Y_train, batch_size = 64, epochs = 15, verbose = 1, validation_data = (X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose = 0)
print('Test loss: ', score[0])
print('Test accuracy:', score[1])
#Page 145