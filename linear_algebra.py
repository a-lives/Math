import sympy as sp
import re

class Vector:
    def __init__(self,*coords):
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
    
    def __getitem__(self,item):
        return self.data[item]
    
    def norm(self):
        return sp.sqrt(sum(x**2 for x in self))
    
    def cross(self,other):
        return Vector(self[1]*other[2]-self[2]*other[1],
                      self[2]*other[0]-self[0]*other[2],
                      self[0]*other[1]-self[1]*other[0],)
    
    @classmethod
    def from_dot(self,fdot,tdot):
        data = []
        for c1,c2 in zip(fdot,tdot):
            data.append(c2-c1)
        return Vector(*data)

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

def vectorial_angle(v1:Vector,v2:Vector):
    return (v1*v2)/(v1.norm()*v2.norm())


class DotBox:
    def __init__(self,dots_name:str,dots_crood:list):
        """ 
        dots_name : likes "A B C A1 B1 C1"
        dots_crood : likes [(0,0,0),(1,2,3)]
        return a DotBox class
        You can use xxx['A'] to get dot A
        """
        self.dotnames = re.findall(r"[^ ]",dots_name)
        self.name2crood = dict()
        for a,b in zip(self.dotnames,dots_crood):
            self.name2crood[a] = b
    
    def __getitem__(self,item):
        return Dot(*self.name2crood[item])

class VectorBox:
    def __init__(self,dotbox:DotBox):
        """ 
        return a VectorBox class
        You can use xxx['AB'] to get vector AB
        """
        self.dotbox = dotbox
    
    def __getitem__(self,item):
        dotnames = re.findall(r"[A-Z]\d*")
        fdot = self.dotbox[dotnames[0]]
        tdot = self.dotbox[dotnames[1]]
        return Vector.from_dot(fdot,tdot)
    
    
class Matrix:
    def __init__(self,matrix):
        pass
    
    @classmethod
    def from_vector(self,vectors):
        pass