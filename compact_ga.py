# Compact Genetic Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import random

def onemax(vector):
  return sum(int(vector[x]) for x in xrange(len(vector)))

def generate_candidate(vector):
  candidate = {}
  candidate["bitstring"] = [0]*len(vector)
  for index,prob in enumerate(vector):
    candidate["bitstring"][index] = 1 if random.random()<prob else 0
  candidate["cost"] = onemax(candidate["bitstring"])
  return candidate

def update_vector(vector,winner,loser,pop_size):
  for i in xrange(len(vector)):  
    if winner["bitstring"][i] != loser["bitstring"][i]:
      if winner["bitstring"][i] == 1:
        vector[i] += 1.0/float(pop_size)
      else:
        vector[i] -= 1.0/float(pop_size)

def search(num_bits=32,max_iterations=200,pop_size=20):
  best = {"cost":0}
  vector = [0.5]*num_bits
  for iter in xrange(max_iterations):
    c1 = generate_candidate(vector)
    c2 = generate_candidate(vector)
    winner,loser = [c1,c2] if c1["cost"] > c2["cost"] else [c2,c1]
    if winner["cost"] > best["cost"]:best = winner 
    update_vector(vector,winner,loser,pop_size)
    print ">iter=%d, f=%d, s=%s" % (iter,best["cost"],''.join(map(str,best["bitstring"])))
    if best["cost"] == num_bits: break 
  return best

if __name__ == '__main__':
  best = search(num_bits=64,max_iterations=500,pop_size=40)
  print ">best: f=%d/%d, s=%s" % (best["cost"],len(best["bitstring"]),''.join(map(str,best["bitstring"])))
