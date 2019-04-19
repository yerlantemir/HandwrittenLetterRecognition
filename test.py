from keras.models import model_from_json
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
import tensorflow as tf

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras.models import load_model
from keras.preprocessing import image

# load json and create model
#json_file = open('model2.json', 'r')


#loaded_model_json = json_file.read()
#json_file.close()
#loaded_model = model_from_json(loaded_model_json)
#
#
## load weights into new model
#loaded_model.load_weights("model2.h5")
#print("Loaded model from disk")
loaded_model = load_model('model.h5')
# 



def rgb2gray(rgb):
    return np.dot(rgb[...,:], [0.2989, 0.5870, 0.1140])


test_image = image.load_img('screen.png',target_size = (28,28))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
test_image = rgb2gray(test_image)
test_image = test_image.reshape(1,28,28,1)
kek = test_image[0].reshape(28,28)
output_values = loaded_model.predict(test_image)
for i in range(output_values.shape[1]):
    if int(output_values[0][i]) == 1:
        print(i)























