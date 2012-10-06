# Grammatical Evolution in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import math,random,operator

def random_bitstring(num_bits):
  return ''.join(random.choice(['0','1']) for i in xrange(num_bits))

def point_mutation(bitstring):
  rate=1.0/float(len(bitstring))
  child = ''
  for i in xrange(len(bitstring)):
    bit = bitstring[i]
    child += ( ('0' if bit=='1' else '1' ) if (random.random()<rate) else bit )
  return child

def one_point_crossover(parent1,parent2,codon_bits,p_cross):
  if random.random()>=p_cross: return parent1 
  cut = random.randint(0,min(len(parent1),len(parent2))/codon_bits)*codon_bits
  return parent1[:cut]+parent2[cut:]
  
def codon_duplication(bitstring,codon_bits):
  rate=1.0/float(codon_bits)
  if random.random() >= rate: return bitstring 
  codons = len(bitstring)/codon_bits  
  idx = random.randint(0,codons)*codon_bits
  return bitstring + bitstring[idx:idx+codon_bits]

def codon_deletion(bitstring,codon_bits):
  rate=0.5/float(codon_bits)
  if random.random() >= rate: return bitstring 
  codons = len(bitstring)/codon_bits  
  idx = random.randint(0,codons)*codon_bits
  return bitstring[:idx] + bitstring[idx+codon_bits:]

def reproduce(selected,pop_size,p_cross,codon_bits):
  children = []
  for i,p1 in enumerate(selected):
    p2 = selected[i+1] if (i%2==0) else selected[i-1]
    child = {}
    child['bitstring'] = one_point_crossover(p1['bitstring'],p2['bitstring'],codon_bits,p_cross)
    child['bitstring'] = codon_deletion(child['bitstring'],codon_bits)
    child['bitstring'] = codon_duplication(child['bitstring'],codon_bits)
    child['bitstring'] = point_mutation(child['bitstring'])
    children.append(child)
  return children

def binary_tournament(pop):
  i, j = random.sample(xrange(len(pop)),2)
  return pop[i] if pop[i]['fitness'] < pop[j]['fitness'] else pop[j]
  
def decode_integers(bitstring,codon_bits):
  ints = []
  for off in xrange(len(bitstring)/codon_bits):
    idx = off*codon_bits
    codon = bitstring[idx:idx+codon_bits]
    sum = 0
    for i in xrange(len(codon)):
      sum += (1 if codon[i]=='1' else 0) * (2 ** i);
    ints.append(sum)
  return ints

def map_(grammar,integers,max_depth):
  done, offset, depth = False, 0, 0
  symbolic_string = grammar['S']
  while not done:
    done = True
    for key in grammar:
      index = 0
      initial_string_len = len(symbolic_string)
      while index < initial_string_len:
        index = symbolic_string.find(key,index)
        if index == -1: break
        done = False
        set = grammar['VAR'] if (key=='EXP' and depth>=max_depth-1) else grammar[key]
        integer = integers[offset] % len(set)
        offset = 0 if (offset==len(integers)-1) else offset+1
        symbolic_string = symbolic_string[:index] + set[integer] + symbolic_string[index+len(key):]
        index += len(key)
    depth += 1
  return symbolic_string

def target_function(x):
  return x**4.0 + x**3.0 + x**2.0 + x
  
def sample_from_bounds(bounds):
  return random.uniform(bounds[0],bounds[1])
  #return bounds[0] + ((bounds[1] - bounds[0]) * random.random())

def cost(program,bounds,num_trials=30):
  if program=='INPUT': return 9999999 
  sum_error = 0.0    
  for _ in xrange(num_trials):
    x = sample_from_bounds(bounds)
    expression = program.replace('INPUT',str(x))
    try: 
      score = eval(expression) 
    except:
      score = float('NaN')
    if math.isnan(score) or math.isinf(score): return 9999999 
    sum_error += abs(score-target_function(x))
  return sum_error / float(num_trials)

def evaluate(candidate,codon_bits,grammar,max_depth,bounds):
  candidate['integers'] = decode_integers(candidate['bitstring'],codon_bits)
  candidate['program'] = map_(grammar,candidate['integers'],max_depth)
  candidate['fitness'] = cost(candidate['program'],bounds)
  
def search(max_gens,pop_size,codon_bits,num_bits,p_cross,grammar,max_depth,bounds):
  pop = [{'bitstring':random_bitstring(num_bits)} for i in xrange(pop_size)]
  for c in pop: evaluate(c,codon_bits,grammar,max_depth,bounds)
  best = sorted(pop,key=operator.itemgetter('fitness'))[-1] # [0] = minimize, [-1] = maximize
  for gen in range(max_gens):
    selected = [binary_tournament(pop) for i in xrange(pop_size)] 
    children = reproduce(selected,pop_size,p_cross,codon_bits)
    for c in children: evaluate(c,codon_bits,grammar,max_depth,bounds)    
    children = sorted(children,key=operator.itemgetter('fitness'))
    if children[-1]['fitness'] >= best['fitness']: best = children[-1] # <= minimize, >= maximize
    pop = sorted((children+pop),key=operator.itemgetter('fitness'))[:pop_size]
    print ' > gen=%d, f=%f\n s=%s' % (gen,best['fitness'],best['program'].replace('and True','').replace('True and ',''))
    if best['fitness']<1e-5: break 
  return best
  
if __name__=='__main__':
  # problem configuration
  grammar = {'S':'EXP',
    'EXP':[' EXP BINARY EXP ', ' (EXP BINARY EXP) ', ' VAR '],
    'BINARY':['+', '-', '/', '*' ],
    'VAR':['INPUT', '1.0']}
  bounds = [1, 10]
  # algorithm configuration
  max_depth = 7
  max_gens = 50
  pop_size = 100
  codon_bits = 4
  num_bits = 10*codon_bits
  p_cross = 0.30
  # execute the algorithm
  best = search(max_gens,pop_size,codon_bits,num_bits,p_cross,grammar,max_depth,bounds)
  print "done! Solution: f={0}, s={1}".format(best['fitness'],best['program'])
