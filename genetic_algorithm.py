# Genetic Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import random,operator

def fitness(bitstring): # OneMax problem. Seeking binary string of all 1's
  return sum(int(bitstring[x]) for x in xrange(len(bitstring)))

def random_bitstring(num_bits):
  return "".join(random.choice("01") for i in xrange(num_bits))	

def binary_tournament(pop):
  i, j = random.sample(xrange(len(pop)),2)
  return pop[i] if pop[i]['fitness'] > pop[j]['fitness'] else pop[j] # < = minimize, > = maximize

def point_mutation(bs,rate):
  return "".join([("0" if bs[i]=="1" else "1") if (random.random()<rate) else bs[i] for i in xrange(len(bs))])
  
def crossover(parent1,parent2,p_crossover):
  if random.random()>=p_crossover: return parent1 
  point = random.randint(1,len(parent1)-1)
  return parent1[:point]+parent2[point:]

def reproduce(selected,p_crossover,p_mutation):
  children = [] 
  for i in xrange(len(selected)-1):
    child = {}
    child["bitstring"] = crossover(selected[i]["bitstring"],selected[i+1]["bitstring"],p_crossover)
    child["bitstring"] = point_mutation(child["bitstring"],p_mutation)
    children.append(child)
  return children
  
def search(max_gens,num_bits,pop_size,p_crossover,p_mutation):
  pop = [{'bitstring':random_bitstring(num_bits)} for i in xrange(pop_size)]  
  for c in pop: c["fitness"] = fitness(c["bitstring"])
  best = sorted(pop,key=operator.itemgetter("fitness"))[-1] # [0] = minimize, [-1] = maximize
  for gen in xrange(max_gens):
    selected = [binary_tournament(pop) for i in xrange(pop_size)] 
    children = reproduce(selected,p_crossover,p_mutation)
    for c in children: c["fitness"] = fitness(c["bitstring"])    
    children = sorted(children,key=operator.itemgetter("fitness"))
    if children[-1]["fitness"] >= best["fitness"]: best=children[-1] # [0] = minimize, [-1] = maximize
    pop = children
    print ">%d: %d, %s" % (gen,best["fitness"],best["bitstring"])
    if best["fitness"]==num_bits: break
  return best
  
if __name__ == '__main__':
  num_bits = 64       # problem configuration
  max_gens = 50       # algorithm configuration
  pop_size = 100
  p_crossover = 0.98
  p_mutation = 1.0/num_bits
  best = search(max_gens,num_bits,pop_size,p_crossover,p_mutation)
  print "best: %d, %s" % (best["fitness"],best["bitstring"])
