import random

class DNASequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.fitness = 0

    def calc_fitness(self, target):
        matches = sum(1 for a, b in zip(self.sequence, target) if a == b)
        self.fitness = matches / len(target)
        return self.fitness

    def mutate(self, mutation_rate=0.01):
        bases = ['A', 'T', 'G', 'C']
        seq_list = list(self.sequence)
        for i in range(len(seq_list)):
            if random.random() < mutation_rate:
                new_base = random.choice(bases)
                while new_base == seq_list[i]:
                    new_base = random.choice(bases)
                seq_list[i] = new_base
        self.sequence = ''.join(seq_list)

class Population:
    def __init__(self, target, pop_size=50, mutation_rate=0.01):
        self.target = target
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.population = [DNASequence(self._random_sequence(len(target))) for _ in range(pop_size)]
        self.generation = 0
        self.best_sequence = None

    def _random_sequence(self, length):
        return ''.join(random.choice(['A', 'T', 'G', 'C']) for _ in range(length))

    def evaluate(self):
        max_fit = 0
        for individual in self.population:
            fit = individual.calc_fitness(self.target)
            if fit > max_fit:
                max_fit = fit
                self.best_sequence = individual.sequence
        return max_fit

    def select(self):
        # Sort population by fitness descending
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        # Keep top 50% as parents
        survivors = self.population[:self.pop_size // 2]
        # Reproduce to refill population
        children = []
        while len(survivors) + len(children) < self.pop_size:
            parent = random.choice(survivors)
            child_seq = parent.sequence
            child = DNASequence(child_seq)
            child.mutate(self.mutation_rate)
            children.append(child)
        self.population = survivors + children

    def evolve(self, max_generations=1000):
        for _ in range(max_generations):
            self.generation += 1
            fitness = self.evaluate()
            print(f"Generation {self.generation} - Best fitness: {fitness:.4f} - Best seq: {self.best_sequence}")
            if fitness == 1.0:
                print("Target sequence evolved!")
                break
            self.select()

if __name__ == "__main__":
    target_dna = "ATGCGTACGTTAGC"
    pop = Population(target=target_dna, pop_size=100, mutation_rate=0.02)
    pop.evolve(max_generations=500)
