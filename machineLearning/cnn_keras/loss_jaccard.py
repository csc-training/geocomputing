# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 06:53:46 2020

@author: ekkylli
Ideas and code from: 
    * https://github.com/CosmiQ/CosmiQ_SN4_Baseline/blob/master/cosmiq_sn4_baseline/losses.py
    * https://gist.github.com/wassname/f1452b748efcbeb4cb9b1d059dce6f96
"""
from tensorflow.keras import backend as K

def jaccard_loss(y_true, y_pred, smooth=100):
    """Jaccard (IoU) loss function for use with Keras.
    Arguments:
    ----------
    y_true (tensor): passed silently by Keras during model training.
    y_pred (tensor): passed silently by Keras during model training.
    Returns:
    --------
    The Jaccard (IoU) loss
    The Jaccard loss, or IoU loss, is defined as:
    1 - intersection(true, pred)/union(true, pred).
    This loss function can be very useful in semantic segmentation problems
    with imbalanced classes.
    """

    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
    jac = (intersection + smooth) / (sum_ - intersection + smooth)
    return (1 - jac) * smooth


def hybrid_bce_jaccard(y_true, y_pred, jac_frac=0.5):
    """Hybrid binary cross-entropy and Jaccard loss function.
    Arguments:
    ----------
    y_true (tensor): passed silently by Keras during model training.
    y_pred (tensor): passed silently by Keras during model training.
    jac_frac (float, range [0, 1]): Fraction of the loss comprised by Jaccard.
        binary cross-entropy will make up the remainder.
    Returns:
    --------
    The hybrid BCE-Jaccard (IoU) loss.
    As with the pure Jaccard loss, this loss function is often used in
    optimization of semantic segmentation problems with imbalanced classes
    where BCE has a strong propensity to fall into a valley of predicting all
    one class. See https://arxiv.org/abs/1806.05182 and others for similar
    approaches.
    """
    jac_loss = jaccard_loss(y_true, y_pred)
    bce = K.binary_crossentropy(y_true, y_pred)

    return jac_frac*jac_loss + (1-jac_frac)*bce