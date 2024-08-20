from bird import Bird

class Bird_Population():
    def __init__(self, pop_size, group):
        self.birds = []
        self.pop_size = pop_size
        for _ in range(self.pop_size):
            self.birds.append(Bird(group))

    def extinct(self):
        extinct = True
        for bird in self.birds:
            if not bird.has_collide:
                extinct = False
        return extinct