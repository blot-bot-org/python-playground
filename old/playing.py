import math

import insutil

start = []
ins = []
for i in range(0, 100):
    ins.append((math.sin(i) * 10 - i, math.cos(i) * 10 + i))

    
insutil.write_instructions(ins)
