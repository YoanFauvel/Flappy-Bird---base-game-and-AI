import random
import operator

class Species():
    def __init__(self, bird):
        self.birds = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.birds.append(bird)
        self.benchmark_fitness = bird.fitness
        self.benchmark_network = bird.network.clone()
        self.champion = bird.clone()
        self.staleness = 0
    
    def similarity(self, network):
        """
            Check if the weight difference between two birds is greater than the threshold value.
        """

        similarity = self.weight_difference(self.benchmark_network, network)
        return self.threshold > similarity
    
    @staticmethod
    def weight_difference(network_1, network_2):
        total_weigh_difference = 0
        for i in range(len(network_1.connections)):
            for j in range(len(network_2.connections)):
                if i == j:
                    total_weigh_difference += abs(network_1.connections[i].weight - network_2.connections[j].weight)
        return total_weigh_difference

    def add_to_species(self, bird):
        self.birds.append(bird)
    
    def sort_bird_by_fitness(self):
        """
            Sort the birds by their fitness value and check if they are progressing.
        """

        self.birds.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.birds[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.birds[0].fitness
            self.champion = self.birds[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for bird in self.birds:
            total_fitness += bird.fitness
        if self.birds:
            self.average_fitness = int(total_fitness / len(self.birds))
        else:
            self.average_fitness = 0

    def offspring(self):
        """
            Create a new bird from an existing one and mutate its network (change of the weights of the network).
        """

        baby = self.birds[random.randint(1, len(self.birds)) - 1].clone()
        baby.network.mutate()
        return baby