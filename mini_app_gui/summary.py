from block1 import add
from block2 import multiply
 
def generate_summary(a, b):
    s = add(a, b)
    m = multiply(a, b)
    return s, m
 