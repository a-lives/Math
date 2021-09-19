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
        return sum(a*b for a,b in zip(self,other))

    def __iter__(self):
        return iter(self.data)
    
    def __str__(self) -> str:
        return str(self.data)
    
    def norm(self):
        return sp.sqrt(sum(x**2 for x in self))
    
def vetorial_angle(v1:Vector,v2:Vector):
    return (v1*v2)/(v1.norm()*v2.norm())
    
    
class Matrix:
    def __init__(self,matrix):
        pass
    
    @classmethod
    def from_vector(self,vectors):
        pass
        
        
        
        
        
if __name__ == "__main__":
    x = sp.symbols('x')
    v1 = Vector([1,2,x])
    v2 = Vector([4,5,6])
    print(vetorial_angle(v1,v2))
    