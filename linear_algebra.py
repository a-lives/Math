from typing import Iterator
import sympy as sp

class Vector:
    def __init__(self,vector):
        self.dim = len(vector)
        self.data = vector
    
    def __add__(self,other):
        vector = []
        for a,b in zip(self,other):
            vector.append(a+b)
        return Vector(vector)
    
    def __sub__(self,other):
        vector = []
        for a,b in zip(self,other):
            vector.append(a-b)
        return Vector(vector)
    
    def __mul__(self,other):
        pass

    def __iter__(self):
        return iter(self.data)
    
    def __str__(self) -> str:
        return str(self.data)
    
class Matrix:
    def __init__(self):
        pass
    
    @classmethod
    def form_vector(self,vectors):
        pass
        
if __name__ == "__main__":
    x = sp.symbols('x')
    v1 = Vector([1,2,x])
    v2 = Vector([4,5,6])
    print(v1+v2)
    