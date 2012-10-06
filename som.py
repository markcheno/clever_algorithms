# Self-Organizing Map Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import math,random

def random_vector(minmax):
  return [random.uniform(minmax[k][0],minmax[k][1]) for k in xrange(len(minmax))]

def initialize_vectors(domain,width,height):
  codebook_vectors = []
  for x in xrange(width):
    for y in xrange(height):
      codebook = {}
      codebook['vector'] = random_vector(domain)
      codebook['coord'] = [x,y] 
      codebook_vectors.append(codebook)
  return codebook_vectors

def euclidean_distance(c1,c2):
  sum = 0.0
  for i in xrange(len(c1)):
    sum += (c1[i]-c2[i])**2.0
  return math.sqrt(sum)

def get_best_matching_unit(codebook_vectors,pattern):
  best,b_dist = None,None
  for codebook in codebook_vectors:
    dist = euclidean_distance(codebook['vector'],pattern)
    if b_dist==None or dist<b_dist:
      best,b_dist = codebook,dist
  return [best,b_dist]

def get_vectors_in_neighborhood(bmu,codebook_vectors,neigh_size):
  neighborhood = []
  for other in codebook_vectors:
    if euclidean_distance(bmu['coord'],other['coord']) <= neigh_size:
      neighborhood.append(other)
  return neighborhood

def update_codebook_vector(codebook,pattern,lrate):
  for i,v in enumerate(codebook['vector']):
    error = pattern[i]-codebook['vector'][i]
    codebook['vector'][i] += lrate * error 

def train_network(vectors,shape,iterations,l_rate,neighborhood_size):
  for iter in xrange(iterations):
    pattern = random_vector(shape)
    lrate = l_rate * (1.0-(float(iter)/float(iterations)))
    neigh_size = neighborhood_size * (1.0-(float(iter)/float(iterations)))
    bmu,dist = get_best_matching_unit(vectors,pattern)
    neighbors = get_vectors_in_neighborhood(bmu,vectors,neigh_size)
    for node in neighbors:
      update_codebook_vector(node,pattern,lrate)
    print ">training: neighbors={0}, bmu_dist={1}".format(len(neighbors),dist)

def summarize_vectors(vectors):
  minmax = [[1,0] for _ in xrange(len(vectors[0]['vector']))]
  for c in vectors:
    for i,v in enumerate(c['vector']):
      if v<minmax[i][0]: minmax[i][0] = v 
      if v>minmax[i][1]: minmax[i][1] = v 
  s = ''
  for i,bounds in enumerate(minmax):
    s += "{0}={1} ".format(i,bounds)
  print "Vector details: {0}".format(s)
  return minmax

def test_network(codebook_vectors,shape,num_trials=100):
  error = 0.0
  for _ in xrange(num_trials):
    pattern = random_vector(shape)
    bmu,dist = get_best_matching_unit(codebook_vectors,pattern)
    error += dist
  error /= float(num_trials)
  print "Finished, average error={0}".format(error) 
  return error

def execute(domain,shape,iterations=100,l_rate=0.3,neigh_size=5,width=4,height=5):
  vectors = initialize_vectors(domain,width,height)
  summarize_vectors(vectors)
  train_network(vectors,shape,iterations,l_rate,neigh_size)
  test_network(vectors,shape)
  summarize_vectors(vectors)
  return vectors

if __name__ == '__main__':
  # problem configuration
  domain = [[0.0,1.0],[0.0,1.0]]
  shape  = [[0.3,0.6],[0.3,0.6]]
  execute(domain,shape)