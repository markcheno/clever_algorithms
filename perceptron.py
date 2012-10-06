# Perceptron Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import random

def random_vector(minmax):
  return [random.uniform(minmax[k][0],minmax[k][1]) for k in xrange(len(minmax))]
  
def initialize_weights(problem_size):
  return random_vector([[-1.0,1.0] for _ in xrange(problem_size+1)])

def update_weights(num_inputs,weights,input,out_exp,out_act,l_rate):
  for i in xrange(num_inputs):
    weights[i] += l_rate * (out_exp-out_act) * input[i]
  weights[num_inputs] += l_rate * (out_exp-out_act) * 1.0
  
def activate(weights,vector):
  sum = weights[-1] * 1.0
  for i,input in enumerate(vector):
    sum += weights[i] * input
  return sum

def transfer(activation):
  return 1.0 if activation>=0 else 0.0

def get_output(weights,vector):
  return transfer(activate(weights,vector))

def train_weights(weights,domain,num_inputs,iterations,lrate):
  for epoch in xrange(iterations):
    error = 0.0
    for pattern in domain:
      input = [float(pattern[k]) for k in xrange(num_inputs)]
      output = get_output(weights,input)
      expected = float(pattern[-1])
      error += abs(output-expected)
      update_weights(num_inputs,weights,input,expected,output,lrate)
    print "> epoch={0}, error={1}".format(epoch,error)
    
def test_weights(weights,domain,num_inputs):
  correct = 0
  for pattern in domain:
    input_vector = [float(pattern[k]) for k in xrange(num_inputs)]
    output = get_output(weights,input_vector)
    if round(output)==pattern[-1]: correct += 1 
  print "Finished test with a score of {0}/{1}".format(correct,len(domain))
  return correct

def execute(domain,num_inputs,iterations,learning_rate):
  weights = initialize_weights(num_inputs)
  train_weights(weights,domain,num_inputs,iterations,learning_rate)
  test_weights(weights,domain,num_inputs)
  return weights

if __name__ == '__main__':
  # problem configuration
  or_problem = [[0,0,0], [0,1,1], [1,0,1], [1,1,1]]
  inputs = 2
  # algorithm configuration
  iterations = 20
  learning_rate = 0.1  
  # execute the algorithm
  execute(or_problem,inputs,iterations,learning_rate)
