from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

train_path = r'./train_set/'
test_path = r'./test_set/'


train_batches = ImageDataGenerator(rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True).flow_from_directory(train_path,target_size=(28,28),
                                   classes='ә,і,ң,ғ,ү,ұ,қ,ө,һ'.split(','))

test_batches = ImageDataGenerator(rescale=1./255).flow_from_directory(test_path,target_size=(28,28),
                                   classes='ә,і,ң,ғ,ү,ұ,қ,ө,һ'.split(','))



def rgb2gray(rgb):
    return np.dot(rgb[...,:], [0.2989, 0.5870, 0.1140])


data_list_x = []
data_list_y = []
batch_index = 0


data_list_x_1 = []
data_list_y_1 = []


while batch_index <= test_batches.batch_index:
    x,y = test_batches.next()
    
    for i in range(len(x)):
        img_data = rgb2gray(x[i])
        data_list_x_1.append(img_data)
        for k in range(y.shape[1]):
            if y[i][k] == 1:
                data_list_y_1.append(k)
    batch_index = batch_index + 1

batch_index = 0
while batch_index <= train_batches.batch_index:
    x,y = train_batches.next()
    
    for i in range(len(x)):
        img_data = rgb2gray(x[i])
        data_list_x.append(img_data)
        for k in range(y.shape[1]):
            if y[i][k] == 1:
                data_list_y.append(k)
    batch_index = batch_index + 1


train_x = np.array(data_list_x).reshape(len(data_list_x),28,28,1).astype('float32')
train_y = np.array(data_list_y).astype('int64')

test_x = np.array(data_list_x_1).reshape(len(data_list_x_1),28,28,1).astype('float32')
test_y = np.array(data_list_y_1).astype('int64')



model = Sequential()
input_shape = (28, 28,1)
model.add(Conv2D(32, kernel_size=(5,5), input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(4,4)))
model.add(Flatten()) # Flattening the 2D arrays for fully connected layers
model.add(Dense(128, activation = tf.nn.relu))
model.add(Dropout(0.2))
model.add(Dense(9,activation=tf.nn.softmax))

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

model.fit(x=train_x,y=train_y, epochs=10)

scores = model.evaluate(test_x, test_y)
print(scores)
print(model.metrics_names)
#model.save('model.h5')

#convolutional

#model_json = model.to_json()
#with open ('model2.json','w') as json_file:
#    json_file.write(model_json)
#model.save_weights('model2.h5')
#print('saved model to disk')







#
#def plots(ims,figsize=(8,6),rows = 1,interp = False , titles=None):
#    if type(ims[0]) is np.ndarray:
#        ims = np.array(ims).astype(np.uint8)
#        if(ims.shape[-1] != 3):
#            ims = ims.transpose(0,2,3,1)
#    f = plt.figure(figsize=figsize)
#    cols = len(ims)//rows if len(ims) % 2 == 0 else len(ims)//rows+1
#    for i in range(len(ims)):
#        sp = f.add_subplot(rows,cols,i+1)
#        sp.axis('Off')
#        if titles is not None:
#            sp.set_title(titles[i],fontsize=16)
#        plt.imshow(ims[i],interpolation=None if interp else 'none')