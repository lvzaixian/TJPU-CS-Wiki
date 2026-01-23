import numpy as np
import scipy
from scipy import linalg

a= np.asmatrix('[2 1 -5 1;1 -3 0 -6;0 2 -1 2;1 4 -7 6]')
b=np.asmatrix('[8;9;-5;0]')
solve = linalg.solve(a, b)
print(solve)
