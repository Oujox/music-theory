import numpy as np

def min_max(x: np.ndarray, axis=None) -> np.ndarray:
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    return 2*(x-min)/(max-min) - 1
