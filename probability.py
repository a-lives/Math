import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from decimal import Decimal

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
        try:
            return int(A(n,m)/A(m,m))
        except:
            return (A(n,m)//A(m,m))
    
    
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
#d=BIN_D(100000,1-10e-5,values=(20-500000,20))  
class BIN_D(PBB_Model):
    """ 二项式分布 """
    def __init__(self,n,p,values=(0,1),acc="symbol"):
        """ 
        acc: "symbol" or an int 
        values: (0,1) or others , 0 ~ p , 1 ~ (1-p)
        """
        self.n = n
        self.p = p
        self.LOPD = []
        self.X = []
        self.P = []
        if acc == "symbol":
            for i in range(self.n+1):
                try:
                    self.LOPD.append((x:= i*values[1] + (self.n-i)*values[0]  , p:=(C(self.n,i) * (self.p**i) * ((1-self.p)**(self.n-i))) ))
                except:
                    self.LOPD.append((x:= i*values[1] + (self.n-i)*values[0]  , p:=(Decimal(C(self.n,i)) * Decimal(self.p**i) * Decimal((1-self.p)**(self.n-i))) ))
                self.X.append(x)
                self.P.append(p)
        else:
            for i in range(self.n+1):
                self.LOPD.append((x:= i*values[1] + (self.n-i)*values[0]  , p:=(C(self.n,i) * (self.p**i) * ((1-self.p)**(self.n-i))*sp.Rational(1,1)).evalf(acc) ))
                self.X.append(x)
                self.P.append(p)
    
    def exp(self):
        return self.n*self.p
    
    def var(self):
        return self.n*self.p*(1-self.p)
    
class HYP_D(PBB_Model):
    """ 超几何分布 """
    def __init__(self,N,M,n,acc="symbol",values=(0,1)):
        """
        acc: "symbol" or an int 
        values: (0,1) or others , 0 ~ p , 1 ~ (1-p)
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
                self.LOPD.append((x:= i*values[1] + (self.n-i)*values[0]  ,p:= sp.Rational(C(self.M,i)*C(self.N-self.M,self.n-i), C(self.N,self.n)) ))
                self.X.append(x)
                self.P.append(p)
        else:
            for i in range(self.m,self.r+1):
                self.LOPD.append((x:= i*values[1] + (self.n-i)*values[0]  ,p:= sp.Rational(C(self.M,i)*C(self.N-self.M,self.n-i), C(self.N,self.n)).evalf(acc) ))
                self.X.append(x)
                self.P.append(p)
            
    def exp(self):
        return self.n * sp.Rational(self.M,self.N)
        
        
class NORM_D:
    """ 
    正态分布
    """
    def __init__(self,mu,sigma):
        self.mu = mu
        self.sigma = sigma
        self.var = sigma**2
        self.x = sp.symbols('x')
        self.E = (1/(sigma*sp.sqrt(2*sp.pi)) ) * sp.E ** -( (self.x-self.mu)**2 / 2*self.var )
        self.IE = sp.integrate(self.E,self.x)
    def get_prob(self,ll=None,ul=None,acc=10):
        if ll == None and ul == None:
            answer  = 1
        if ll == None and not ul == None:
            answer = (self.IE.subs(self.x,ul) + 0.5).evalf(acc)
        if not ll == None and ul == None:
            answer = (0.5 - self.IE.subs(self.x,ll)).evalf(acc)
        if not ll == None and not ul == None:
            answer = (self.IE.subs(self.x,ul) - self.IE.subs(self.x,ll)).evalf(acc)
        return answer
    

