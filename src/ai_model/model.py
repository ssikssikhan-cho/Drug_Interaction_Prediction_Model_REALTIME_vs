class SimpleModel:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self.build_model()

    def build_model(self):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout

        model = Sequential()
        model.add(Dense(128, activation='relu', input_shape=self.input_shape))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

    def save_model(self, filepath):
        self.model.save(filepath)

    def load_model(self, filepath):
        from tensorflow.keras.models import load_model
        self.model = load_model(filepath)