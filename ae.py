import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_privacy as tfp


#niveis            = [nv1, nv2, nv3    ]
#niveis de epsilon = [0.5, 1.0, 2.0    ]
#niveis de ruido   = [1.059, 0.8, 0.625]

X_ae = pd.read_csv("ae_train.csv").values

noise_m=0.625
opt=tfp.privacy.optimizers.dp_optimizer_keras.DPKerasAdamOptimizer(
    l2_norm_clip=1.3,
    noise_multiplier=noise_m,
    num_microbatches=1,
)

from tensorflow.keras import layers, models

def create_autoencoder(input_size, encoding_dim):
    input_layer = tf.keras.Input(shape=(input_size,))
    encoded = layers.Dense(64, activation='relu')(input_layer)
    encoded = layers.Dense(64, activation='relu')(encoded)
    encoded = layers.Dense(32, activation='relu')(encoded)
    encoded = layers.Dense(encoding_dim, activation='relu')(encoded)

    decoded = layers.Dense(32, activation='relu')(encoded)
    decoded = layers.Dense(64, activation='relu')(decoded)
    decoded = layers.Dense(64, activation='relu')(decoded)
    decoded = layers.Dense(input_size, activation='sigmoid')(decoded)

    autoencoder = models.Model(inputs=input_layer, outputs=decoded)

    return autoencoder

autoencoder = create_autoencoder(12, 16)
autoencoder.compile(optimizer=opt, loss='mse')
history = autoencoder.fit(
    X_ae, X_ae,
    epochs=10,
    batch_size=128,
    shuffle=True,
    validation_split=0.2
)