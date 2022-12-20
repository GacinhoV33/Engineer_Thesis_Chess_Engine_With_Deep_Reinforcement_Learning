#!/usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf
from keras.losses import CategoricalCrossentropy, MeanSquaredError
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, ReLU, BatchNormalization, add, GlobalAveragePooling2D
from tensorflow.keras.models import load_model
""" 64 × 8 × 7 = 3584 Queen-like moves and  64 × 8 = 512(356) knight-like moves 
(4x6 + 4x5 + 16x4 + 4x4 + 16x2 ->impossible knight moves from end of board)
Overall: 4672(4516) outputs
"""
NUMBER_OF_CONSIDERED_POSITIONS = 8 # TODO if compute hard, change it to smaller number
NUMBER_OF_POSSIBLE_MOVES = 4672
INPUT_SHAPE = (19, 8, 8)
batch_size = 8 #?


def create_network(save_model: bool = True):
    input = Input(shape=INPUT_SHAPE, name='PositionEvaluationModel')

    """block 1"""
    b1_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same', use_bias='false', name='b1_conv2d_1', kernel_initializer='normal')(input)
    b1_relu_1 = ReLU(name='b1_relu_1')(b1_conv2D_1)
    b1_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b1_bn_1')(b1_relu_1)

    b1_conv2D_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b1_conv2D_2', kernel_initializer='normal')(b1_bn_1)
    b1_relu_2 = ReLU(name='b1_relu_2')(b1_conv2D_2)
    b1_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b1_out')(b1_relu_2)  # size: 14*14

    """block 2"""
    b2_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same', use_bias=False, name='b2_conv2D_1')(b1_out)
    b2_relu_1 = ReLU(name='b2_relu_1')(b2_conv2D_1)
    b2_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b2_bn_1')(b2_relu_1)

    b2_add = add([b1_out, b2_bn_1])

    b2_conv2D_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b2_conv2D_2', kernel_initializer='normal')(b2_add)
    b2_relu_2 = ReLU(name='b2_relu_2')(b2_conv2D_2)
    b2_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b2_bn_2')(b2_relu_2)

    """block 3"""
    b3_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b3_conv2D_1', kernel_initializer='normal')(b2_out)

    b3_relu_1 = ReLU(name='b3_relu_1')(b3_conv2D_1)
    b3_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b3_bn_1')(b3_relu_1)  # size: 7*7

    b3_add = add([b2_out, b3_bn_1])  #

    b3_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b3_cnv2d_2', kernel_initializer='normal')(b3_add)
    b3_relu_2 = ReLU(name='b3_relu_2')(b3_cnv2d_2)
    b3_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b3_out')(b3_relu_2)

    """block 4"""
    b4_avg_p = GlobalAveragePooling2D()(b3_out)

    """Output"""
    flatten = Flatten()(b4_avg_p)
    pre_value = Dense(256)(flatten)

    policy_head = Dense(NUMBER_OF_POSSIBLE_MOVES, name='policy_head', activation='softmax', kernel_initializer='he_uniform')(flatten)
    value_head = Dense(1, activation='tanh', name='value_head')(pre_value)
    output = [policy_head, value_head]
    model = Model(inputs=input, outputs=output)

    model.compile(optimizer='adam', loss={'policy_head': CategoricalCrossentropy(),
                                          'value_head': MeanSquaredError()} )
    model_json = model.to_json()

    with open("./models/sample_res_net_vo.json", "w") as json_file:
        json_file.write(model_json)
    model.summary()

    if save_model:
        model.save('./models/basic_model.keras')

    return model


def load_existing_model(name: str = 'basic_model'):
    try:
        return load_model('./models/' + name + '.keras')
    except FileNotFoundError as e:
        print('Error during loading model.')


create_network(True)
model = load_existing_model()
model.summary()
