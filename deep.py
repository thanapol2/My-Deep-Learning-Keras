from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import np_utils
plt.rcParams['figure.figsize'] = (7,7)

nb_classes = 10

(X_train, y_train), (X_test, y_test) = mnist.load_data()
print("X_train original shape", X_train.shape)
print("y_train original shape", y_train.shape)
# plt.interactive(False)
#
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(X_train[i], cmap='gray', interpolation='none')
    plt.title("Class {}".format(y_train[i]))

plt.show()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()
model.add(Dense(512, input_shape=(784,)))
model.add(Activation('relu'))

model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(X_train, Y_train,
          batch_size=128, nb_epoch=4,
          validation_data=(X_test, Y_test))

prediction = model.predict_classes(X_test)

correctResult = np.nonzero(prediction == y_test)[0]
incorrectResult = np.nonzero(prediction != y_test)[0]

plt.figure()
for i, correct in enumerate(correctResult[:9]):
    plt.subplot(3, 3, i + 1)
    plt.imshow(X_test[correct].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title("Predicted {}, Class {}".format(prediction[correct], y_test[correct]))

plt.figure()
for i, incorrect in enumerate(incorrectResult[:9]):
    plt.subplot(3, 3, i + 1)
    plt.imshow(X_test[incorrect].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title("Predicted {}, Class {}".format(prediction[incorrect], y_test[incorrect]))

plt.show()