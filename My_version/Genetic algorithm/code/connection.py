import random

class Connection():
    def __init__(self, input_neuron, output_neuron, weight):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.weight = weight
    
    def mutate_weight(self):
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1) / 10
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1 
    
    def clone(self, input_neuron, output_neuron):
        clone = Connection(input_neuron, output_neuron, self.weight)
        return clone
