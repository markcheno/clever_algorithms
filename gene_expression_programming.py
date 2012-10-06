# Genetic Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import math,random,operator

def binary_tournament(pop):
  i,j = random.sample(xrange(len(pop)),2)
  return pop[i] if pop[i]['fitness'] < pop[j]['fitness'] else pop[j]

def point_mutation(grammar,genome,head_length):
  rate = 1.0/float(len(genome))
  child = ''
  for i in xrange(len(genome)):
    bit = genome[i]
    if random.random() < rate:
      if i < head_length:
        selection = grammar['FUNC'] if (random.random() < 0.5) else grammar['TERM']
        bit = selection[random.randint(0,len(selection)-1)]
      else:
        bit = grammar['TERM'][random.randint(0,len(grammar['TERM'])-1)]
    child += bit
  return child

def crossover(parent1,parent2,p_crossover):
  if random.random()<p_crossover: return parent1 
  return ''.join([parent1[i] if (random.random()<0.5) else parent2[i] for i in xrange(len(parent1))])

def reproduce(grammar,selected,pop_size,p_crossover,head_length):
  children = []
  for i,p1 in enumerate(selected):
    p2 = selected[i+1] if (i%2==0) else selected[i-1]
    if i==len(selected)-1: p2 = selected[0] 
    child = {}
    child['genome'] = crossover(p1['genome'],p2['genome'],p_crossover)
    child['genome'] = point_mutation(grammar,child['genome'],head_length)
    children.append(child)
  return children

def random_genome(grammar,head_length,tail_length):
  s = ''
  for _ in xrange(head_length):
    selection = grammar['FUNC'] if (random.random() < 0.5) else grammar['TERM']
    s += selection[random.randint(0,len(selection)-1)]
  s += ''.join([grammar['TERM'][random.randint(0,len(grammar['TERM'])-1)] for _ in range(tail_length)])
  return s

def cost(program,bounds,num_trials=30):
  errors = 0.0
  for _ in range(num_trials):
    x = random.uniform(bounds[0],bounds[1])
    expression,score = program.replace("x", str(x)),0.0
    try:
      score = eval(expression) 
    except:
      score = float('Nan')
    if math.isnan(score) or math.isinf(score): return 1E38
    target = x**4.0 + x**3.0 + x**2.0 + x
    errors += abs(score-target)
  return errors / float(num_trials)

def mapping(genome,grammar):
  off,queue,root = 0,[],{}
  root['node'] = genome[off]
  off+=1
  queue.append(root)
  while not len(queue)==0:
    current = queue.pop(0)
    if grammar['FUNC'].count(current['node'])>0:
      current['left'] = {}
      current['left']['node'] = genome[off]
      off+=1 
      queue.append(current['left'])
      current['right'] = {}
      current['right']['node'] = genome[off]
      off+=1
      queue.append(current['right'])
  return root

def tree_to_string(exp):
  if (not('left' in exp)) or (not('right' in exp)): return exp['node']
  left = tree_to_string(exp['left'])
  right = tree_to_string(exp['right'])
  return "({0} {1} {2})".format(left,exp['node'],right)

def evaluate(candidate,grammar,bounds):
  candidate['expression'] = mapping(candidate['genome'],grammar)
  candidate['program'] = tree_to_string(candidate['expression'])
  candidate['fitness'] = cost(candidate['program'],bounds)

def search(grammar,bounds,h_length,t_length,max_gens,pop_size,p_cross):
  pop = [{'genome':random_genome(grammar,h_length,t_length)} for _ in xrange(pop_size)]
  for c in pop: evaluate(c,grammar,bounds)  
  best = sorted(pop,key=operator.itemgetter("fitness"))[0] # [0] = minimize, [-1] = maximize
  for gen in xrange(max_gens):
    selected = [binary_tournament(pop) for i in xrange(pop_size)] 
    children = reproduce(grammar,selected,pop_size,p_cross,h_length)    
    for c in children: evaluate(c,grammar,bounds)
    children = sorted(children,key=operator.itemgetter("fitness"))
    if children[0]["fitness"] <= best["fitness"]: best=children[0] # [0] = minimize, [-1] = maximize
    pop = children+pop
    pop = pop[:pop_size]
    print " > gen={0}, f={1}, g={2} p={3}".format(gen,best['fitness'],best['genome'],best['program'])
    if best['fitness'] < 1e-5: break
  return best

if __name__ == '__main__':
  # problem configuration
  grammar = {"FUNC":["+","-","*","/"], "TERM":["x"]}
  bounds = [1.0, 10.0]
  # algorithm configuration
  h_length = 20
  t_length = 21
  max_gens = 250
  pop_size = 80
  p_cross = 0.85
  # execute the algorithm
  best = search(grammar,bounds,h_length,t_length,max_gens,pop_size,p_cross)
  print "done! Solution: f={0}, program={1}".format(best['fitness'],best['program'])
