import random

def genetic_algorithm(start, goal, population_size=100, generations=500, mutation_rate=0.1, log_callback=None):

    def fitness(state):
        dist = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_index = goal.index(val)
                row_s, col_s = divmod(i, 3)
                row_g, col_g = divmod(goal_index, 3)
                dist += abs(row_s - row_g) + abs(col_s - col_g)
        return dist

    def crossover(p1, p2):
        child = [-1] * 9
        start, end = sorted(random.sample(range(9), 2))
        child[start:end+1] = p1[start:end+1]
        pointer = 0
        for i in range(9):
            if child[i] == -1:
                while p2[pointer] in child:
                    pointer += 1
                child[i] = p2[pointer]
        return tuple(child)

    def mutate(state):
        s = list(state)
        i, j = random.sample([x for x in range(9) if s[x] != 0], 2)
        s[i], s[j] = s[j], s[i]
        return tuple(s)

    def is_solvable(state):
        inv = 0
        arr = [x for x in state if x != 0]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0

    # --- STEP 1: Initialize Population ---
    population = []
    while len(population) < population_size:
        shuffled = list(start)
        random.shuffle(shuffled)
        candidate = tuple(shuffled)
        if is_solvable(candidate):
            population.append(candidate)

    expansions = 0

    # --- STEP 2 to End: Loop over generations ---
    for gen in range(generations):
        # Evaluate fitness
        population.sort(key=lambda s: fitness(s))
        best = population[0]
        best_fitness = fitness(best)

        if log_callback:
            log_callback(f"[GA] Thế hệ {gen+1} – Cá thể tốt nhất: {best_fitness}")

        # Solution found
        if best_fitness == 0:
            return [start, best], expansions

        # Mate individuals (tạo thế hệ mới)
        next_gen = population[:10]  # elitism: giữ top 10

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:50], 2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                child = mutate(child)
            if is_solvable(child):
                next_gen.append(child)
            expansions += 1

        population = next_gen  # Cập nhật quần thể

    return None, expansions  # Không tìm thấy lời giải