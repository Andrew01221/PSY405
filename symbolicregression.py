import pysr
import numpy as np
from matplotlib import pyplot as plt
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
import os

# Positive experiences equation: 0.7165598 - 0.0072595254*x0 0.717 - 0.00726 x_{0}
# Negative experience equation: 2.42295201233914*exp(x1*(0.002637848*x0 + 0.0380654432322184)) (2.42 e^{x_{1} \cdot \left(0.00264 x_{0} + 0.0381\right)})


# data here

x_and_y = np.array([[1,100],[2,50],[4,25],[100,1],[10,20],[40,5]]) # number of people and total magnitude of the experience in the aforementioned format (np.

# Negative: [1,-100],[2,-50],[4,-25],[100,-1],[10,-20],[40,-5]
# Positive: [1,100],[2,50],[4,25],[100,1],[10,20],[40,5]



'''[2, -100], [4, -50], [8, -25], [10, -20],[20,-10], 
[40, -5], [50, -4], [100, -2], [1,-100],[2,-50], 
[4,-25], [5,-20], [10,-10], [20,-5], [50,-2], [100,-1]'''

'''For the survey, need the following items:
[4, -100], [5, -80], [8, -50], [10, -40], [16, -25], [20, -20], [25, -16], [40, -10], [50, -8], [80, -5], [100, -4], [200, -2], [400, -1] 
[2, -100], [4, -50], [8, -25], [10, -20],[20, -10], [25, -8], [40, -5], [50, -4], [100, -2], [200, -1]
[1, -100],[2, -50], [4, -25], [5, -20], [10, -10], [20, -5], [25, -4], [50, -2], [100, -1]
'''

'''
GET PARTIAL DERIVATIVES TO INTERPRET FUNCTION AND CONNECT TO PAST LITERATURE
BREAK DOWN INTO SE AND IE
'''

z = np.array([0.6821518741143225, 0.7843482367668508, 0.5014700815745397, 0.0, 0.8170498241535389, 0.37459408906407454]) # utility value goes here (in order ofc)
# Positive: [0.6821518741143225, 0.7843482367668508, 0.5014700815745397, 0.0, 0.8170498241535389, 0.37459408906407454]
# Negative: [0.0, 0.2998137475760408, 0.6977045469406676, 1.8167381642247795, 0.6825735647958119, 1.1849986248486388]







# https://www.desmos.com/3d/16b0u3lm1x

 
# print(X)
# print(X[:, 0]) # egts all of the first values in each row

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

# https://www.desmos.com/3d/dlp6xx7ysh for graphs

# https://www.youtube.com/watch?v=q6tjKXmhiMs 
# https://colab.research.google.com/drive/1x2nB_l1Rb9z3Vd-wU2gq44LOCYtMS8xc#scrollTo=vFpyRxmhFqeH

# https://github.com/MilesCranmer/pysr_wandb 

# Questions for Niles Cranmer

# Previous output:
# 0.00642 x_{1} \left(x_{0} + 1.35\right) + 5.90 e^{x_{1}} + 1.48
# 0.00654 x_{0} x_{1} + 0.00887 x_{1} + 5.88 e^{x_{1}} + 1.50

# FIGURE OUT HOW TO MODEL WITH BOUNDS ON X (MUST BE POSITIVE) AND Y (COLLECTIVE MUST NOT EXCEED -100 or 100)
# CREATE SEPARATE GRAPHS FOR POSITIVE AND NEGATIVE EXPERIENCES AND CREATE ONE THAT ENCPASULATES BOTH SETS OF DATA AND COMPARE TO SEE IF THEY ARE FUNDAMENTALLY DIFFERENT
# LOOK INTO PARAMETER SETTING FOR SYMBOLIC REGRESSION
# Maybe test the model's predictions with actual people