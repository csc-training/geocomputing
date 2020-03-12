# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:07:18 2020

@author: ekkylli
Code mainly from https://solaris.readthedocs.io/en/latest/tutorials/notebooks/api_training_custom.html
Added comments and option to train multiclass labels.
"""

from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose
from tensorflow.keras.layers import concatenate
from tensorflow.keras import Model

# TODO If training data has different amount of channels, modify input_shape accordingly, for example for 5 channels: input_shape=(512, 512, 5)
# Something else too? I guess no?

def cosmiq_sn4_baseline(input_shape=(512, 512, 3), base_depth=64, no_of_classes=2):
    """Keras implementation of untrained TernausNet model architecture.

    Arguments:
    ----------
    input_shape (3-tuple): a tuple defining the shape of the input image.
    base_depth (int): the base convolution filter depth for the first layer
        of the model. Must be divisible by two, as the final layer uses
        base_depth/2 filters. The default value, 64, corresponds to the
        original TernausNetV1 depth.
    no_of_classes: an interger - how many classes the labels have.

    Returns:
    --------
    An uncompiled Keras Model instance with TernausNetV1 architecture.

    """
    inputs = Input(input_shape)

    # Convolution wtih Conv2D and MaxPooling2D layers.
    # TODO. 3 here is the window size of 3x3 pixels. Any comments on using for example 5x5 window? Unusual?
    conv1 = Conv2D(base_depth, 3, activation='relu', padding='same')(inputs) #No of pixels: 512x512
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1) #256x256

    conv2_1 = Conv2D(base_depth*2, 3, activation='relu',
                     padding='same')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2_1) #128x128

    conv3_1 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(pool2)
    conv3_2 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(conv3_1)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3_2) #64x64

    conv4_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool3)
    conv4_2 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(conv4_1)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4_2) #32x32

    conv5_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool4)
    conv5_2 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(conv5_1)
    pool5 = MaxPooling2D(pool_size=(2, 2))(conv5_2) #16x16
    
    # The middle layer, biggest number of filters and smallest number of pixels
    conv6_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool5)

    # Deconvolution with Conv2DTranspose and Conv2D layers.
    up7 = Conv2DTranspose(base_depth*4, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv6_1)
    concat7 = concatenate([up7, conv5_2]) #32x32
    conv7_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(concat7)

    up8 = Conv2DTranspose(base_depth*4, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv7_1)
    concat8 = concatenate([up8, conv4_2]) #64x64
    conv8_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(concat8)

    up9 = Conv2DTranspose(base_depth*2, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv8_1)
    concat9 = concatenate([up9, conv3_2]) #128x128
    conv9_1 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(concat9)

    up10 = Conv2DTranspose(base_depth, 2, strides=(2, 2), activation='relu',
                           padding='same')(conv9_1)
    concat10 = concatenate([up10, conv2_1]) #256x256
    conv10_1 = Conv2D(base_depth*2, 3, activation='relu',
                      padding='same')(concat10)

    up11 = Conv2DTranspose(int(base_depth/2), 2, strides=(2, 2),
                           activation='relu', padding='same')(conv10_1)
    concat11 = concatenate([up11, conv1]) #512x512
    
    # Set the last layer size and activation function according to how many classes the labels have.
    if no_of_classes == 2: 
        activation='sigmoid' 
        out_layers = 1
    else:
        activation='softmax'
        out_layers = no_of_classes
    out = Conv2D(out_layers, 1, activation=activation, padding='same')(concat11)

    return Model(inputs=inputs, outputs=out)