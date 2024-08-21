from neuron import Neuron
from connection import Connection
import random

class Network():
    def __init__(self, inputs: int, clone:bool = False):
        self.connections = []
        self.neurons = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            # create input neurons
            for i in range(self.inputs):
                self.neurons.append(Neuron(id_number=i))
                self.neurons[i].layer = 0
            
            # create bias neuron
            self.neurons.append(Neuron(3))
            self.neurons[3].layer = 0

            # create output layer
            self.neurons.append(Neuron(4))
            self.neurons[4].layer = 1

            # create connections
            for i in range(4):
                self.connections.append(Connection(input_neuron=self.neurons[i], output_neuron=self.neurons[4], weight=random.uniform(-1,1)))

    def connect_neurons(self):
        for i in range(len(self.neurons)):
            self.neurons[i].connections = []
        
        for i in range(len(self.connections)):
            self.connections[i].input_neuron.connections.append(self.connections[i])

    def generate_network(self):
        self.connect_neurons()
        self.net = []
        for i in range(self.layers):
            for j in range(len(self.neurons)):
                if self.neurons[j].layer == i:
                    self.net.append(self.neurons[j])

    def feed_forward(self, vision: list):
        for i in range(self.inputs):
            self.neurons[i].output_value = vision[i]
        self.neurons[3].output_value = 1

        for i in range(len(self.net)):
            self.net[i].activate()

        output_value = self.neurons[4].output_value

        for i in range(len(self.neurons)):
            self.neurons[i].input_value = 0

        return output_value
    
    def clone(self):
        clone = Network(self.inputs, True)
        for neuron in self.neurons:
            clone.neurons.append(neuron.clone())

        for connection in self.connections:
            clone.connections.append(connection.clone(clone.getNeuron(connection.input_neuron.id), clone.getNeuron(connection.output_neuron.id)))

        clone.layers = self.layers
        clone.connect_neurons()
        return clone

    def getNeuron(self, id):
        for neuron in self.neurons:
            if neuron.id == id:
                return neuron
            
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(len(self.connections)):
                self.connections[i].mutate_weight()