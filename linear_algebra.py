import sympy as sp

class Vector:
    def __init__(self,coords):
        vector = []
        for c in coords:
            vector.append(c)
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
    
    @classmethod
    def from_dot(self,fdot,tdot):
        data = []
        for c1,c2 in zip(fdot,tdot):
            data.append(c2-c1)
        return Vector(data)

class Dot:
    def __init__(self,*coords) -> None:
        coord = []
        for c in coords:
            coord.append(c)
        self.coord = coord
        
    def __str__(self) -> str:
        return str(self.coord)
    
    def __iter__(self):
        return iter(self.coord)

def vetorial_angle(v1:Vector,v2:Vector):
    return (v1*v2)/(v1.norm()*v2.norm())
    
    
class Matrix:
    def __init__(self,matrix):
        pass
    
    @classmethod
    def from_vector(self,vectors):
        pass
    