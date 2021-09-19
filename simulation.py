import numpy as np
import matplotlib.pyplot as plt
import random
import re
import time

from numpy.core.fromnumeric import sort

class Genes:
    def __init__(self,autosome:str,allosome:str):
        self.autosome_genes = re.findall(r"\w{2,2}",autosome)
        self.autosome_genes_str = autosome
        self.allosome_genes = allosome
    def __str__(self):
        autosome = ""
        for gene in self.autosome_genes:
            autosome = autosome+gene
        return autosome+self.allosome_genes
        
class Animal:
    def __init__(self,genes:Genes,name=None,order=None):
        self.name = name
        self.genes = genes
        if order==None:
            self.order = time.time()
        allosome = self.genes.allosome_genes
        if allosome == "XY":
            self.sex = "male"
        elif allosome == "XX":
            self.sex = "female"
    def gametogenesis(self):
        ng = ""
        for g in self.genes.autosome_genes:
            ng += g[random.randint(0,1)]
        ng += self.genes.allosome_genes[random.randint(0,1)]
        return ng

class Polulation:
    def __init__(self,animals,sexual=True,fecundity=[1,4]):
        self.animals = animals
        self.sexual = sexual
        self.fecundity = fecundity #繁殖能力:[int,int]闭区间 表示每对配偶产生后代数
        if sexual:
            self.male = []
            self.female = []
            for animal in self.animals:
                if animal.sex == "male":
                    self.male.append(animal)
                else:
                    self.female.append(animal)
    def mutiply(self):
        if self.sexual:
            #初始化种群
            new_male_animals = []
            new_female_animals = []
            
            #随机配对
            amount = min(len(self.male),len(self.female))
            males = random.sample(self.male,amount)
            females = random.sample(self.female,amount)
            
            #繁衍行为
            for m,f in zip(males,females):
                for _ in range(random.randint(self.fecundity[0],self.fecundity[1])):
                    #新基因型
                    ng = ""
                    for mg,fg in zip(m.gametogenesis(),f.gametogenesis()):
                        ng += "".join(sort([mg,fg]))
                    #加入种群
                    newone = Animal(Genes(ng[:-2],ng[-2:]),order=time.time())
                    if newone.sex == 'male':
                        new_male_animals.append(newone)
                    else:
                        new_female_animals.append(newone)
            
            #种群更新
            self.male = new_male_animals
            self.female = new_female_animals
            self.animals = self.male + self.female
    
    def statistic_sex(self):
        print("male:%d\tfemale:%d" % (len(self.male),len(self.female)))
        return len(self.male),len(self.female)
    
    def statistic_genetype(self,sexual=False,print_=True):
        if sexual:
            males = dict()
            females = dict()
            for animal in self.animals:
                if animal.sex == "male":
                    try:
                        males[animal.genes.autosome_genes_str] += 1
                    except:
                        males[animal.genes.autosome_genes_str] = 1
                else:
                    try:
                        females[animal.genes.autosome_genes_str] += 1
                    except:
                        females[animal.genes.autosome_genes_str] = 1

            if print_:
                print("*"*20)
                print("male:")
                for key,value in zip(males.keys(),males.values()):
                    print(key,":",value)
                print("female:")
                for key,value in zip(females.keys(),females.values()):
                    print(key,":",value) 
                print("*"*20)
            
            return males,females
        else:
            allanimal = dict()
            for animal in self.animals:
                try:
                    allanimal[animal.genes.autosome_genes_str] += 1
                except:
                    allanimal[animal.genes.autosome_genes_str] = 1
            if print_:
                print("*"*20)
                allanimal_ = sorted(allanimal.items())
                for key,value in allanimal_:
                    print(key,":",value)
                print("*"*20)
            
            return allanimal
        
def cat_simu():        
    genes_1 = Genes("aaBb","XY")
    genes_2 = Genes("AaBb","XX")
    cats = []
    for i in range(50):
        cats.append(Animal(genes_1,order=time.time()))
    for _ in range(100):
        cats.append(Animal(genes_2,order=time.time()))
    polu = Polulation(cats,fecundity=[1,4])
    iteration = {}
    for _ in range(24):
        print(_)
        polu.mutiply()
        genetype = polu.statistic_genetype(print_=False)
        for g in genetype.items():
            try:
                iteration[g[0]].append(g[1])
            except:
                iteration[g[0]] = [g[1],]
    for i in list(iteration.items()):
        plt.plot( range(1,len(i[1])+1) , i[1] , label=i[0])

cat_simu()
plt.legend()
plt.show()