# Backpropagation Algorithm in the Python Programming Language

# Based on: The Clever Algorithms Project: http://www.CleverAlgorithms.com
# (c) Copyright 2012 Mark Chenoweth. 
# This work is licensed under a Creative Commons Attribution-Noncommercial-Share License.

import math,random

def random_vector(minmax):
  return [random.uniform(minmax[k][0],minmax[k][1]) for k in xrange(len(minmax))]

def initialize_weights(num_weights):
  minmax = [[-random.random(),random.random()] for _ in xrange(num_weights)]
  return random_vector(minmax)

def activate(weights,vector):
  sum = weights[-1] * 1.0
  for i,input in enumerate(vector):
    sum += weights[i] * input
  return sum

def transfer(activation):
  return 1.0 / (1.0 + math.exp(-activation)) 

def transfer_derivative(output):
  return output * (1.0 - output)

def forward_propagate(net,vector):
  for i,layer in enumerate(net):
    input=vector if i==0 else [ net[i-1][k]['output'] for k in xrange(len(net[i-1]))]
    for neuron in layer:
      neuron['activation'] = activate(neuron['weights'],input)
      neuron['output'] = transfer(neuron['activation'])
  return net[-1][0]['output']

def backward_propagate_error(network,expected_output):
  for n in xrange(len(network)):
    index = len(network)-1 -n
    if index==len(network)-1:
      neuron = network[index][0] # assume one node in output layer
      error = (expected_output-neuron['output'])
      neuron['delta'] = error * transfer_derivative(neuron['output'])
    else:
      for k,neuron in enumerate(network[index]):
        sum = 0.0
        # only sum errors weighted by connection to the current k'th neuron
        for next_neuron in network[index+1]:
          sum += (next_neuron['weights'][k] * next_neuron['delta'])
        neuron['delta'] = sum*transfer_derivative(neuron['output'])

def calculate_error_derivatives_for_weights(net,vector):
  for i,layer in enumerate(net):
    input=vector if i==0 else [ net[i-1][k]['output'] for k in xrange(len(net[i-1]))]
    for neuron in layer:
      for j,signal in enumerate(input):
        neuron['deriv'][j] += neuron['delta'] * signal
      neuron['deriv'][-1] += neuron['delta'] * 1.0

def update_weights(network,lrate,mom=0.8):
  for layer in network:
    for neuron in layer:
      for j,w in enumerate(neuron['weights']):
        delta = (lrate * neuron['deriv'][j]) + (neuron['last_delta'][j] * mom)
        neuron['weights'][j] += delta
        neuron['last_delta'][j] = delta
        neuron['deriv'][j] = 0.0

def train_network(network,domain,num_inputs,iterations,lrate):
  correct = 0
  for epoch in xrange(iterations):
    for pattern in domain:
      vector,expected = [float(pattern[k]) for k in range(num_inputs)],pattern[-1]
      output = forward_propagate(network,vector)
      if round(output)==expected: correct += 1
      backward_propagate_error(network,expected)
      calculate_error_derivatives_for_weights(network,vector)
    update_weights(network,lrate)
    if (epoch+1)%100 == 0:
      print "> epoch={0}, Correct={1}/{2}".format(epoch+1,correct,100*len(domain))
      correct = 0

def test_network(network,domain,num_inputs):
  correct = 0
  for pattern in domain:
    input_vector = [float(pattern[k]) for k in xrange(num_inputs)]
    output = forward_propagate(network,input_vector)
    if round(output)==pattern[-1]: correct += 1 
  print "Finished test with a score of {0}/{1}".format(correct,len(domain))
  return correct

def create_neuron(num_inputs):
  return {'weights':initialize_weights(num_inputs+1), 
          'last_delta':[0.0]*(num_inputs+1),
          'deriv':[0.0]*(num_inputs+1)}

def execute(domain,num_inputs,iterations=2000,num_hidden_nodes=4,learning_rate=0.3):
  network = []
  network.append([create_neuron(num_inputs) for _ in range(num_hidden_nodes)])
  network.append([create_neuron(len(network[-1]))])
  print "Topology: {0} {1}".format(num_inputs,' '.join([str(len(network[i])) for i in xrange(len(network))]))
  train_network(network,domain,num_inputs,iterations,learning_rate)  
  test_network(network,domain,num_inputs)
  return network

if __name__ == '__main__':
  # problem configuration
  xor = [[0,0,0], [0,1,1], [1,0,1], [1,1,0]]
  inputs = 2
  execute(xor,inputs)
