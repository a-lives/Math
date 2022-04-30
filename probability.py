import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

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
    
    
class PBB_Model:
    """ 
    LOPD: list of tuple [(x_1,p_1),(x_2,p_2)...]
    X:X's eval,list
    P:P's eval,list
    """
    def __init__(self,LOPD):
        self.X = [x[0] for x in LOPD]
        self.P = [x[1] for x in LOPD]
        self.LOPD = list(LOPD)
        
    def __str__(self) -> str:
        return str(self.LOPD)
        
    def exp(self):
        """ 期望 """
        return sum([x*y for x,y in self.LOPD])
    
    def var(self):
        """ 方差 """
        return sum(x**2*y for x,y in self.LOPD) - self.exp()**2
    
    def std(self):
        """ 标准差 """
        return sp.sqrt(self.var())
    
    def draw(self,type="bar",p_color=None,b_color=None):
        """ 
        type: "plot","bar","all"
        """
        fig,ax = plt.subplots()
        if type == "plot" or type =="all":
            ax.plot(self.X,self.P,color=p_color)
        if type == "bar" or type =="all":
            ax.bar(self.X,self.P,color=b_color)
        return fig
    
class BIN_D(PBB_Model):
    """ 二项式分布 """
    def __init__(self,n,p):
        self.n = n
        self.p = p
        self.LOPD = []
        self.X = []
        self.P = []
        for i in range(self.n+1):
            self.LOPD.append((i , p:=C(self.n,i) * (self.p**i) * ((1-self.p)**(self.n-i)) ))
            self.X.append(i)
            self.P.append(p)
    
    def exp(self):
        return self.n*self.p
    
    def var(self):
        return self.n*self.p*(1-self.p)
    
class HYP_D(PBB_Model):
    """ 超几何分布 """
    def __init__(self,N,M,n,acc="symbol"):
        """
        acc: "symbol" or an int 
        """
        self.N = N
        self.M = M
        self.n = n
        self.m = max(0,self.n-self.N+self.M)
        self.r = min(self.n,self.M)
        self.LOPD = []
        self.X = []
        self.P = []
        if acc == "symbol":    
            for i in range(self.m,self.r+1):
                self.LOPD.append((i ,p:= sp.Rational(C(self.M,i)*C(self.N-self.M,self.n-i), C(self.N,self.n)) ))
                self.X.append(i)
                self.P.append(p)
        else:
            for i in range(self.m,self.r+1):
                self.LOPD.append((i ,p:= sp.Rational(C(self.M,i)*C(self.N-self.M,self.n-i), C(self.N,self.n)).evalf(acc) ))
                self.X.append(i)
                self.P.append(p)
            
    def exp(self):
        return self.n * sp.Rational(self.M,self.N)
        
        
    

