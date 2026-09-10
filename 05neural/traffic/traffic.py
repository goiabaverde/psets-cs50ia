import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    dir_path = os.path.join(data_dir) # Take the path to the directory that contais the data

    NUM_CATEGORIES = sum(os.path.isdir(os.path.join(dir_path, f)) for f in os.listdir(dir_path)) # Count the number of categories

    # Inicialize the lists
    images = []
    labels = []

    # Read the data and save on the lists
    for i in range(NUM_CATEGORIES):
        dir_image_path = os.path.join(f"{str(dir_path)}/{str(i)}")
        for image in os.listdir(os.path.join(dir_image_path)):
            path_image = os.path.join(dir_image_path, image)
            image = cv2.imread(path_image)
            resized_img = cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH))
            image = resized_img.reshape(IMG_HEIGHT, IMG_WIDTH, 3)
            images.append(image/255)
            labels.append(i)

    return (tuple(images), tuple(labels))




def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

        # Covolutional and pooling process
        tf.keras.layers.Conv2D(16, (5,5), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),

        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        tf.keras.layers.Conv2D(20, (5,5), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),

        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        tf.keras.layers.Flatten(),

        # Create the hidden layers
        tf.keras.layers.Dense(120, activation="sigmoid"),
        tf.keras.layers.Dense(84, activation="sigmoid"),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy", "recall"]
)
    return model


if __name__ == "__main__":
    main()
