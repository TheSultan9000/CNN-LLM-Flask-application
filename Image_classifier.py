#  Import packages
import numpy as np
import tensorflow as tf
from keras.models import load_model

def image_classifier(input):
    '''Passes an image through a pre-defined CNN and returns a list of Tags
    Expects: Tensor image
    Modification: Resize the image to 256, 256, and the pixel values are scaled between 0 and 1
    Return: List: Probabilites which are converted toa list of strings: Animal, Building or Nature
    '''
    img_tensor = tf.image.decode_image(input)
    # Image re-sizing
    resize = tf.image.resize(img_tensor, (256, 256))
    model = load_model('CNN.h5')
    # Pixel value scaling
    result = model.predict(np.expand_dims(resize/255, 0))
    # Only the top two tags which have a probability >= 0.1 are processed
    indices = np.argsort(result[0])[-2:]
    tags = []
    for i in indices:
        if result[0][i] >= 0.1:
            if i == 0:
                tags.append("Animal")
            if i == 1:
                tags.append("Building")
            if i == 2:
                tags.append("Nature")

    return tags
