import numpy as np

x = np.array([0,10,27,35,44,32,56,35,87,22,47,17,18])
x = x[0:x.size:2]
print(x)
# [10 27 44 32 35 87 47 17]