#!/usr/bin/python
# -*- coding: utf-8 -*-

from settings import NUMBER_OF_POSSIBLE_MOVES, INPUT_SHAPE
from keras.losses import CategoricalCrossentropy, MeanSquaredError
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, ReLU, BatchNormalization, add, GlobalAveragePooling2D
from tensorflow.keras.models import load_model
""" 64 × 8 × 7 = 3584 Queen-like moves and  64 × 8 = 512(356) knight-like moves 
(4x6 + 4x5 + 16x4 + 4x4 + 16x2 ->impossible knight moves from end of board)
Overall: 4672(4516) outputs
"""


def create_network(save_model: bool = True):
    input = Input(shape=INPUT_SHAPE, name='PositionEvaluationModel')

    """block 1"""
    b1_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same', use_bias='false', name='b1_conv2d_1', kernel_initializer='random_normal', input_shape=INPUT_SHAPE)(input)
    b1_relu_1 = ReLU(name='b1_relu_1')(b1_conv2D_1)
    b1_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b1_bn_1')(b1_relu_1)

    b1_conv2D_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b1_conv2D_2', kernel_initializer='random_normal')(b1_bn_1)
    b1_relu_2 = ReLU(name='b1_relu_2')(b1_conv2D_2)
    b1_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b1_out')(b1_relu_2)  # size: 14*14

    """block 2"""
    b2_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same', use_bias=False, name='b2_conv2D_1')(b1_out)
    b2_relu_1 = ReLU(name='b2_relu_1')(b2_conv2D_1)
    b2_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b2_bn_1')(b2_relu_1)

    b2_add = add([b1_out, b2_bn_1])

    b2_conv2D_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b2_conv2D_2', kernel_initializer='random_normal')(b2_add)
    b2_relu_2 = ReLU(name='b2_relu_2')(b2_conv2D_2)
    b2_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b2_bn_2')(b2_relu_2)

    """block 3"""
    b3_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b3_conv2D_1', kernel_initializer='normal')(b2_out)

    b3_relu_1 = ReLU(name='b3_relu_1')(b3_conv2D_1)
    b3_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b3_bn_1')(b3_relu_1)  # size: 7*7

    b3_add = add([b2_out, b3_bn_1])  #

    b3_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b3_cnv2d_2', kernel_initializer='random_normal')(b3_add)
    b3_relu_2 = ReLU(name='b3_relu_2')(b3_cnv2d_2)
    b3_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b3_out')(b3_relu_2)

    """block 4"""
    b4_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b4_conv2D_1', kernel_initializer='random_normal')(b3_out)

    b4_relu_1 = ReLU(name='b4_relu_1')(b4_conv2D_1)
    b4_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b4_bn_1')(b4_relu_1)  # size: 7*7

    b4_add = add([b3_out, b4_bn_1])  #

    b4_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b4_cnv2d_2', kernel_initializer='random_normal')(b4_add)
    b4_relu_2 = ReLU(name='b4_relu_2')(b4_cnv2d_2)
    b4_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b4_out')(b4_relu_2)

    """block 5"""
    b5_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b5_conv2D_1', kernel_initializer='random_normal')(b4_out)

    b5_relu_1 = ReLU(name='b5_relu_1')(b5_conv2D_1)
    b5_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b5_bn_1')(b5_relu_1)  # size: 7*7

    b5_add = add([b4_out, b5_bn_1])  #

    b5_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b5_cnv2d_2', kernel_initializer='random_normal')(b5_add)
    b5_relu_2 = ReLU(name='b5_relu_2')(b5_cnv2d_2)
    b5_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b5_out')(b5_relu_2)

    """block 6"""
    b6_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b6_conv2D_1', kernel_initializer='random_normal')(b5_out)

    b6_relu_1 = ReLU(name='b6_relu_1')(b6_conv2D_1)
    b6_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b6_bn_1')(b6_relu_1)  # size: 7*7

    b6_add = add([b5_out, b6_bn_1])  #

    b6_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b6_cnv2d_2', kernel_initializer='random_normal')(b6_add)
    b6_relu_2 = ReLU(name='b6_relu_2')(b6_cnv2d_2)
    b6_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b6_out')(b6_relu_2)

    """block 7"""
    b7_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b7_conv2D_1', kernel_initializer='random_normal')(b6_out)

    b7_relu_1 = ReLU(name='b7_relu_1')(b7_conv2D_1)
    b7_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b7_bn_1')(b7_relu_1)  # size: 7*7

    b7_add = add([b6_out, b7_bn_1])  #

    b7_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b7_cnv2d_2', kernel_initializer='random_normal')(b7_add)
    b7_relu_2 = ReLU(name='b7_relu_2')(b7_cnv2d_2)
    b7_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b7_out')(b7_relu_2)

    """block 8"""
    b8_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b8_conv2D_1', kernel_initializer='random_normal')(b7_out)

    b8_relu_1 = ReLU(name='b8_relu_1')(b8_conv2D_1)
    b8_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b8_bn_1')(b8_relu_1)  # size: 7*7

    b8_add = add([b7_out, b8_bn_1])  #

    b8_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b8_cnv2d_2', kernel_initializer='random_normal')(b8_add)
    b8_relu_2 = ReLU(name='b8_relu_2')(b8_cnv2d_2)
    b8_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b8_out')(b8_relu_2)

    """block 9"""
    b9_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b9_conv2D_1', kernel_initializer='random_normal')(b8_out)

    b9_relu_1 = ReLU(name='b9_relu_1')(b9_conv2D_1)
    b9_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b9_bn_1')(b9_relu_1)  # size: 7*7

    b9_add = add([b8_out, b9_bn_1])  #

    b9_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b9_cnv2d_2', kernel_initializer='random_normal')(b9_add)
    b9_relu_2 = ReLU(name='b9_relu_2')(b9_cnv2d_2)
    b9_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b9_out')(b9_relu_2)

    """block 10"""
    b10_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b10_conv2D_1', kernel_initializer='random_normal')(b9_out)

    b10_relu_1 = ReLU(name='b10_relu_1')(b10_conv2D_1)
    b10_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b10_bn_1')(b10_relu_1)  # size: 7*7

    b10_add = add([b9_out, b10_bn_1])  #

    b10_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                        use_bias=False, name='b10_cnv2d_2', kernel_initializer='random_normal')(b10_add)
    b10_relu_2 = ReLU(name='b10_relu_2')(b10_cnv2d_2)
    b10_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b10_out')(b10_relu_2)
    """block 11"""
    b11_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                          use_bias=False, name='b11_conv2D_1', kernel_initializer='random_normal')(b10_out)

    b11_relu_1 = ReLU(name='b11_relu_1')(b11_conv2D_1)
    b11_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b11_bn_1')(b11_relu_1)  # size: 7*7

    b11_add = add([b10_out, b11_bn_1])  #

    b11_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b11_cnv2d_2', kernel_initializer='random_normal')(b11_add)
    b11_relu_2 = ReLU(name='b11_relu_2')(b11_cnv2d_2)
    b11_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b11_out')(b11_relu_2)
    """block 12"""
    b12_conv2D_1 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                          use_bias=False, name='b12_conv2D_1', kernel_initializer='random_normal')(b11_out)

    b12_relu_1 = ReLU(name='b12_relu_1')(b12_conv2D_1)
    b12_bn_1 = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b12_bn_1')(b12_relu_1)  # size: 7*7

    b12_add = add([b11_out, b12_bn_1])  #

    b12_cnv2d_2 = Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same',
                         use_bias=False, name='b12_cnv2d_2', kernel_initializer='random_normal')(b12_add)
    b12_relu_2 = ReLU(name='b12_relu_2')(b12_cnv2d_2)
    b12_out = BatchNormalization(epsilon=1e-3, momentum=0.999, name='b12_out')(b12_relu_2)
    """Pooling """
    b13_avg_p = GlobalAveragePooling2D()(b12_out)

    """Output"""
    flatten = Flatten()(b13_avg_p)
    pre_value = Dense(256)(flatten)

    policy_head = Dense(NUMBER_OF_POSSIBLE_MOVES, name='policy_head', activation='softmax', kernel_initializer='random_normal')(flatten)
    value_head = Dense(1, activation='tanh', name='value_head', kernel_initializer='random_normal')(pre_value)
    output = [policy_head, value_head]
    model = Model(inputs=input, outputs=output)

    model.compile(optimizer='adam', loss={'policy_head': CategoricalCrossentropy(),
                                          'value_head': MeanSquaredError()} )
    model_json = model.to_json()

    with open("./models/sample_res_net_vo.json", "w") as json_file:
        json_file.write(model_json)
    model.summary()

    if save_model:
        model.save('./models/model_12_res.keras')

    return model


def load_existing_model(name: str = 'model_12_res'):
    try:
        return load_model('./models/' + name + '.keras')
    except FileNotFoundError as e:
        print('Error during loading model.')


if __name__ == "__main__":
    create_network(True)
    model = load_existing_model()
    model.summary()

