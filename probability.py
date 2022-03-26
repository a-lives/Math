import numpy as np
import matplotlib.pyplot as plt

def multiplicative(a,b):
    """ 
    a<=b
    return a*(a+1)*...*b
    if a==b :return 1
    """
    if a==b:
        return a
    else:
        z = 1
        for i in range(a,b+1,1):
            z*=i
        return z    

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

def A(n:int,m:int)->int:
    """ 
    arrangement
    """
    if n<=0 or m <0:
        print("Error:   n:",n,"m:",m)
        return None
    if n==m:
        return factorial(n)
    elif m==0:
        return 1
    else:
        return multiplicative(n-m+1,n)

def C(n:int,m:int)->int:
    """ 
    combination
    """
    if n<=0 or m <0:
        print("Error:   n:",n,"m:",m)
        return None
    if m==0:
        return 1
    else:
        return int(A(n,m)/A(m,m))