import pysr
import numpy as np
from matplotlib import pyplot as plt
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
import os

x_and_y = np.array([[1,100],[2,50],[4,25],[100,1],[10,20],[40,5]]) # number of people and total magnitude of the experience in the aforementioned format (np.

z = np.array([0.6821518741143225, 0.7843482367668508, 0.5014700815745397, 0.0, 0.8170498241535389, 0.37459408906407454]) # utility value goes here (in order ofc)

default_pysr_params = dict(
    populations = 30, # 3*(os.cpu_count())
    model_selection = "best",
    # procs = os.cpu_count()
    # parsimony = 0.2
    # nested constraints and constraints
    # weight_optimize 
)


model = PySRRegressor(
    niterations = 30,
    binary_operators = ["+", "*"],
    unary_operators = ["exp"],
    **default_pysr_params,
)


'''
model = PySRRegressor(
    niterations = 30,
        binary_operators=["myotherfunction(x, y) = x^2*y"],
    unary_operators = [],
    extra_sympy_mappings={
        "myotherfunction": lambda x, y: x**2 * y,
    },
    **default_pysr_params,
)
'''

model.fit(x_and_y, z)

print(model.sympy())
print(model.latex())
