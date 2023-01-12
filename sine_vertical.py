import numpy as np
import math

in_value = np.linspace(start = -np.pi, stop = np.pi, num = 500)
gain = 50
origin = 50
out_value = gain*np.sin(in_value)

for out in out_value:
    final = math.floor(out) + origin
    for i in range(0, final):
        print(" ", end = "")
    print("*")
