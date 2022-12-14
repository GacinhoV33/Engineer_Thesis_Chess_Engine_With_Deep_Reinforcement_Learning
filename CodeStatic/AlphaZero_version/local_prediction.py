#!/usr/bin/python
# -*- coding: utf-8 -*-
import tensorflow as tf

@tf.function
def predict_local(model, args):
    return model(args)