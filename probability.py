import numpy as np
import matplotlib.pyplot as plt
import sys   
sys.setrecursionlimit(10000) 

def factorial(x:int)->int:
    """ 
    请不要乱输数字
    """
    if x<0 or type(x) != int:
        print("Error: ",x," is not a factorial number")
        return
    if x == 1 or x==0:
        return 1
    else:
        return x*factorial(x-1)

def A(m:int,n:int)->int:
    """ 
    arrangement
    """
    return int(factorial(n)/factorial(n-m))

def C(m:int,n:int)->int:
    """ 
    combination
    """
    return int( factorial(n) / (factorial(m)*factorial(n-m)) )

