# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:07:18 2020

@author: ekkylli
"""

from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose
from tensorflow.keras.layers import concatenate, BatchNormalization, Dropout
from tensorflow.keras import Model

def cosmiq_sn4_baseline(input_shape=(512, 512, 3), base_depth=64, no_of_classes=1):
    """Keras implementation of untrained TernausNet model architecture.

    Arguments:
    ----------
    input_shape (3-tuple): a tuple defining the shape of the input image.
    base_depth (int): the base convolution filter depth for the first layer
        of the model. Must be divisible by two, as the final layer uses
        base_depth/2 filters. The default value, 64, corresponds to the
        original TernausNetV1 depth.

    Returns:
    --------
    An uncompiled Keras Model instance with TernausNetV1 architecture.

    """
    inputs = Input(input_shape)
    conv1 = Conv2D(base_depth, 3, activation='relu', padding='same')(inputs)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2_1 = Conv2D(base_depth*2, 3, activation='relu',
                     padding='same')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2_1)

    conv3_1 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(pool2)
    conv3_2 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(conv3_1)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3_2)

    conv4_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool3)
    conv4_2 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(conv4_1)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4_2)

    conv5_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool4)
    conv5_2 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(conv5_1)
    pool5 = MaxPooling2D(pool_size=(2, 2))(conv5_2)

    conv6_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(pool5)

    up7 = Conv2DTranspose(base_depth*4, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv6_1)
    concat7 = concatenate([up7, conv5_2])
    conv7_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(concat7)

    up8 = Conv2DTranspose(base_depth*4, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv7_1)
    concat8 = concatenate([up8, conv4_2])
    conv8_1 = Conv2D(base_depth*8, 3, activation='relu',
                     padding='same')(concat8)

    up9 = Conv2DTranspose(base_depth*2, 2, strides=(2, 2), activation='relu',
                          padding='same')(conv8_1)
    concat9 = concatenate([up9, conv3_2])
    conv9_1 = Conv2D(base_depth*4, 3, activation='relu',
                     padding='same')(concat9)

    up10 = Conv2DTranspose(base_depth, 2, strides=(2, 2), activation='relu',
                           padding='same')(conv9_1)
    concat10 = concatenate([up10, conv2_1])
    conv10_1 = Conv2D(base_depth*2, 3, activation='relu',
                      padding='same')(concat10)

    up11 = Conv2DTranspose(int(base_depth/2), 2, strides=(2, 2),
                           activation='relu', padding='same')(conv10_1)
    concat11 = concatenate([up11, conv1])
    
    if no_of_classes == 1: 
        activation='sigmoid'  
    else:
        activation='softmax'
    out = Conv2D(no_of_classes, 1, activation=activation, padding='same')(concat11)

    return Model(inputs=inputs, outputs=out)