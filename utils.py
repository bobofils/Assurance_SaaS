import numpy as np
import joblib
import os

def load_model():
    return joblib.load("model.pkl")


def preprocess(age, revenu, couverture):
    return np.array([[age, revenu, couverture]])