import numpy as np
import json
import random
import time
from evolution import Evolution
import selection 
import manage 
# main class for eoh
class EOH:
    # initilization
    def __init__(self, problem, **kwargs):
        self.problem= problem
        self.evolution  = Evolution()
        self.select = selection
        self.ops = ["e1","e2","m1","m2","m3"]
        self.num_gens = 2
        self.manage= manage
        self.population_size = 5
        self.m=2
    def get_alg(self, population, operator):
        """
        Thực hiện toán tử operator trên population
        Returns:
            parents,
            offspring = {
            'algorithm': ,
            'code': ,
            'objective': ,
        }
        """
        offspring = {
            'algorithm': None,
            'code': None,
            'objective': None
        }
        
        if operator == "init":
            parents = None
            code, algorithm =  self.evolution.i1()
        elif operator == "e1":
            parents = self.select.parent_selection(population,self.m)
            [code, algorithm] = self.evolution.e1(parents)
        elif operator == "e2":
            parents = self.select.parent_selection(population,self.m)
            [code, algorithm] = self.evolution.e2(parents) 
        elif operator == "m1":
            parents = self.select.parent_selection(population,1)
            [code, algorithm] = self.evolution.m1(parents[0])   
        elif operator == "m2":
            parents = self.select.parent_selection(population,1)
            [code, algorithm] = self.evolution.m2(parents[0]) 
        elif operator == "m3":
            parents = self.select.parent_selection(population,1)
            [code, algorithm] = self.evolution.m3(parents[0]) 
        else:
            print(f"Evolution operator [{operator}] has not been implemented ! \n") 

        if len(code) == 0:
            print("No code")
            print("Return None")
            return offspring
        
        for ind in population:
            if code == ind['code']:
                print("Duplicated code")
                print("Return None")
                return offspring

        offspring['algorithm']=algorithm
        offspring['code']=code

        #Evaluate
        
        fitness = self.problem.evaluate(code)
        offspring['objective']=np.round(fitness, 5)
        return parents,offspring


    def population_generation(self, n_create=2):
        """
        Init population
        """
        population = []
        for i in range(n_create):
            _,offspring = self.get_alg([],'init')
            
            population.append(offspring)

        return population
    
    def add_population(self,population,offspring):
        """
        Thêm offspring vào population
        """
        #for off in offspring:
        for ind in population:
            if ind['objective'] == offspring['objective']:
                
                print("duplicated result, retrying ... ")
        population.append(offspring)
    
    def run(self):
        print("----------------Start---------------")
        # initialization
        population = []
        print("creating initial population:")
        population = self.population_generation()
        print("Init ",len(population)," ")
        for i in range(self.num_gens):
            print("Generation:",i+1)
            for op in self.ops:
                print("Operator:",op)
                parents,offspring = self.get_alg(population,op)
                self.add_population(population,offspring)
                size_pop = min(len(population), self.population_size)
                population = self.manage.population_management(population, size_pop)
            print("Best fitness:",population[0]['objective'])

        
