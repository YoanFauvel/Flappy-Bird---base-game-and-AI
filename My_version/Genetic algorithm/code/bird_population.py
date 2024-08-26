import math
import operator
from bird import Bird
from species import Species

class Bird_Population():
    def __init__(self, pop_size, group):
        self.birds = []
        self.generation = 1
        self.species = []
        self.pop_size = pop_size
        for _ in range(self.pop_size):
            self.birds.append(Bird(group))

    def natural_selection(self):
        # print("SPECIATE")
        self.speciate()
        print(f"Number of species: {len(self.species)}")

        # print("CALCULATE FITNESS")
        self.calculate_fitness()
        print(f"Best average fitness score: {max([s.average_fitness for s in self.species])}")
        print("\n-----------------------------------\n")
        for idx, s in enumerate(self.species):
            print(f"{len(s.birds)} birds in species number {idx} with average fitness of {s.average_fitness}")
        print("\n-----------------------------------\n")

        # print('KILL EXTINCT')
        self.kill_extinct_species()

        # print('KILL STALE')
        self.kill_stale_species()

        # print("SORT BY FITNESS")
        self.sort_species_by_fitness()

        # print("CHILDREN FOR NEXT GEN")
        self.next_gen()

    def speciate(self):
        """
            Adds the birds to a species if the weights of network do not get bigger than a threshold value, i.e., if they are similar.
        """

        for s in self.species:
            s.birds = []
        for bird in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similarity(bird.network):
                    s.add_to_species(bird)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(Species(bird))

    def calculate_fitness(self):
        """
            Self explanatory name...
        """

        for bird in self.birds:
            bird.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        """
            Self explanatory name...
        """

        species_bin = []
        for s in self.species:
            if len(s.birds) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        """
            Self explanatory name. Kill species that do not show any progress (decided with a threshold value).
        """

        bird_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for bird in self.birds:
                        bird_bin.append(bird)
                else:
                    s.staleness = 0
        for bird in self.birds:
            self.birds.remove(bird)
        for s in species_bin:
            self.species.remove(s)
    
    def sort_species_by_fitness(self):
        """
            Put the species with the best average fitness at the beginning of self.species
        """

        for s in self.species:
            s.sort_bird_by_fitness()
        
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        """
            Function that generate a new generation of bird. To do so, it clones the best birds of each species, then fill in the gap of bird population with new birds
        """

        children = []
        for s in self.species:
            children.append(s.champion.clone())

        children_per_species = math.floor((self.pop_size - len(self.species)) / len(self.species))
        for s in self.species:
            for _ in range(children_per_species):
                children.append(s.offspring())

        while len(children) < self.pop_size:
            children.append(self.species[0].offspring())
        

        self.birds = []
        for child in children:
            self.birds.append(child)
        self.generation += 1

    def extinct(self):
        """
            Check if the total population is extinct.
        """

        extinct = True
        for bird in self.birds:
            if not bird.has_collide:
                extinct = False
        return extinct