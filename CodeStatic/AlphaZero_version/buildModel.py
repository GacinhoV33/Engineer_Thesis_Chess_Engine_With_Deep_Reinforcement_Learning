#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, Flatten, Conv2D, BatchNormalization, LeakyReLU, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import add as add_layer
from tensorflow.keras.models import Model
from tensorflow.python.keras.engine.keras_tensor import KerasTensor
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

from tensorflow.python.framework.ops import disable_eager_execution

from AlphaZero_version import config


class BuildModel:
    def __init__(self, input_shape: tuple, output_shape: tuple):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.nr_hidden_layers = config.AMOUNT_OF_RESIDUAL_BLOCKS
        self.convolution_filters = config.CONVOLUTION_FILTERS

    def build_model(self) -> Model:
        main_input = Input(shape=self.input_shape, name="Main_Input")
        x = self.build_convolutional_layer(main_input)

        for i in range(self.nr_hidden_layers):
            x = self.build_residual_layer(x)
        # model = Model(inputs=main_input, outputs=x)
        policy_head = self.build_policy_head()
        value_head = self.build_value_head()

        model = Model(inputs=main_input, outputs=[policy_head(x), value_head(x)])

        model.compile(loss={'policy_head' : 'categorical_crossentropy', 'value_head' : 'mean_squared_error'})
        return model

    def build_convolutional_layer(self, input_layer) -> KerasTensor:
        layer = Conv2D(filters=self.convolution_filters, kernel_size=(3, 3), strides=(1, 1), padding='same', data_format='channels_first', use_bias=False)(input_layer)
        layer = BatchNormalization(axis=1)(layer)
        layer = Activation('relu')(layer)
        return (layer)

    def build_residual_layer(self, input_layer) -> KerasTensor:
        layer = self.build_convolutional_layer(input_layer)
        layer = Conv2D(filters=self.convolution_filters, kernel_size=(3, 3), strides=(1, 1), padding='same', data_format='channels_first', use_bias=False)(layer)
        layer = BatchNormalization(axis=1)(layer)

        layer = Activation('relu')(layer)
        return (layer)

    def build_policy_head(self) -> Model:
        """
        Builds the policy head of the neural network
        """
        model = Sequential(name='policy_head')
        model.add(Conv2D(2, kernel_size=(1, 1), strides=(1, 1), input_shape=(self.convolution_filters,
                                                                             self.input_shape[1], self.input_shape[2]),
                         padding='same', data_format='channels_first'))
        model.add(BatchNormalization(axis=1))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(self.output_shape[0], activation="sigmoid", name='policy_head'))
        return model

    def build_value_head(self) -> Model:
        """
        Builds the value head of the neural network
        """
        model = Sequential(name='value_head')
        model.add(Conv2D(1, kernel_size=(1, 1), strides=(1, 1),
                         input_shape=(self.convolution_filters,
                                      self.input_shape[1], self.input_shape[2]),
                         padding='same', data_format='channels_first'))
        model.add(BatchNormalization(axis=1))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        # output shape == 1, because we want 1 value: the estimated outcome from the position
        # tanh activation function maps the output to [-1, 1]
        model.add(Dense(self.output_shape[1],
                        activation='tanh', name='value_head'))
        return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create the neural network for chess.')
    parser.add_argument('--model-folder', type=str, default='/models', help='Folder to save the model')
    parser.add_argument('--model-name', type=str, default='model', help='Name of the model (without extension)')

    args = parser.parse_args()
    args = vars(args)

    model_builder = BuildModel(input_shape=config.INPUT_SHAPE, output_shape=config.OUTPUT_SHAPE)
    model = model_builder.build_model()

    if not os.path.exists(args['model_folder']):
        os.makedirs(args['model_folder'])

    print(f"Saving model to {args['model_folder']} as {args['model_name']}.h5 ...")
    # model.save(os.path.join(args['model_folder'], args['model_name']) + '.h5')
    print(model.summary())
    model.save('./models/my_model.h5')
