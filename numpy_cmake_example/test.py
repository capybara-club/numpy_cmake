import numpy as np
from numpy_cmake_example import add_arrays

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])

result = add_arrays(a, b)
print(result)  # Output: [5. 7. 9.]