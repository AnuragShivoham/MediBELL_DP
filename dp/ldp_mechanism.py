import numpy as np
import math
import pandas as pd

def apply_laplace_ldp(X, epsilon):
    """
    Apply Local Differential Privacy using Laplace mechanism
    Assumes numeric, bounded features
    """
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")

    scale = 1.0 / epsilon
    noise = np.random.laplace(0, scale, X.shape)

    X_noisy = X + noise
    X_noisy[X_noisy < 0] = 0  # keep domain valid

    return X_noisy

def randomized_response(val, epsilon=1.0):
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")
    p_keep = math.exp(epsilon) / (math.exp(epsilon) + 1)
    if np.random.rand() < p_keep:
        return val
    else:
        return 1 - val

def apply_ldp(df, epsilon=1.0):
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")
    p_keep = math.exp(epsilon) / (math.exp(epsilon) + 1)
    rand = np.random.rand(*df.shape)
    flipped = 1 - df
    return pd.DataFrame(np.where(rand < p_keep, df, flipped), columns=df.columns, index=df.index)

