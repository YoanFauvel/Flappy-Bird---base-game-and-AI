import math

def sigmoid(x):
            return 1 / (1 + math.exp(-x))

class Neuron():
    def __init__(self, id_number: int):
        self.id = id_number
        self.layer = 0
        self.input_value = 0
        self.output_value = 0
        self.connections = []

    def activate(self):
        """
            Check the position of the neuron in the network and apply to it either a weighted sum or a sigmoid activation function.
        """
    
        if self.layer == 1:
            self.output_value = sigmoid(self.input_value)

        for i in range(len(self.connections)):
            self.connections[i].output_neuron.input_value += self.connections[i].weight * self.output_value

    def clone(self):
         clone = Neuron(self.id)
         clone.id = self.id
         clone.layer = self.layer
         return clone