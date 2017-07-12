## Travelling Salesman problem using genetic algorithm

import random
from sys import stdout
import numpy


def generate_knapsack(total, b, v):
    benefits = []
    volume = []
    sum = 0
    for i in range(0, total):
        benefits.append(random.randint(1, b))
        volume.append(random.randint(1, v))
        sum += volume[i]
    return [benefits, volume, sum]


def print_knapsack(n):
    for i in range(0, n):
        stdout.write("%5d" % i)
    stdout.write("\n")
    for i in range(0, n):
        stdout.write("%5d" % benefits[i])
    stdout.write("\n")
    for i in range(0, n):
        stdout.write("%5d" % volume[i])
    stdout.write("\n")


def not_unique(s):
    s = str(s)
    try:
        t = unique[s]
        return True
    except:
        return False


def to_binary(number, l):
    temp = ""
    j = 0
    while number != 0:
        temp += str(number % 2)
        number /= 2
        j += 1

    for i in range(j, l):
        temp += "0"

    return temp[::-1]


def generate_chromosomes():
    l = len(volume)
    for i in range(0, l):
        s = random.randint(1, 2**l-1)
        while not_unique(s):
            s = random.randint(1, 2**l-1)
        item = str(s)
        unique[item] = 1
        binary = to_binary(s, l)
        chromosomes.append(binary)
        fitting.append(s)


def calculate(chromosome):
    l = len(chromosome)
    total_weight = 0
    total_benefits = 0
    for i in range(0, l):
        if chromosome[i] == '1':
            total_benefits += benefits[i]
            total_weight += volume[i]
    return [total_benefits, total_weight]


def not_selected(chromosome, item):
    if chromosome[item] == "0":
        return True
    return False


def fitness():
    l = len(chromosomes)
    for i in range(0, l):
        knapsack = calculate(chromosomes[i])
        while knapsack[1] > knapsack_capacity:
            item = random.randint(0, total_items - 1)
            # print item
            while not_selected(chromosomes[i], item):
                item = random.randint(1, total_items - 1)
                # print item
            # new = ""
            # if item == 0:
            #     new = "0" + chromosomes[i][1:]
            # elif item == total_items - 1:
            #     new = chromosomes[i][:item] + "0"
            # else:
            new = chromosomes[i][:item] + "0" + chromosomes[i][item+1:]
            chromosomes[i] = new
            knapsack = calculate(chromosomes[i])
        curr_benefits.append(knapsack[0])
        curr_volumes.append(knapsack[1])


# select individual using roulette wheel selection
def roulette_selection():
    r = random.randint(0, volume_sum - 1)

    for i in range(0, total_items):
        r -= volume[i]
        if r <= 0:
            return i


# select individuals for reproduction
def select():
    n1 = roulette_selection()
    n2 = n1
    while n2 == n1:
        n2 = roulette_selection()
    # print ""
    # print n1, n2
    # print chromosomes[n1], "    ", chromosomes[n2]
    # print ""
    c = [chromosomes[n1], chromosomes[n2]]
    # indices = [n1, n2]
    return [[n1, n2], c]


# perform single point crossover
def crossover():
    parent1 = selected[0]
    parent2 = selected[1]
    crossover_point = random.randint(0, total_items - 1)

    p = numpy.random.binomial(1, crossover_rate)
    if p:
        child1 = parent1[:crossover_point + 1] + parent2[crossover_point + 1:]
        child2 = parent2[:crossover_point + 1] + parent1[crossover_point + 1:]
        # print 1, crossover_point, len(parent1), len(parent2)
    else:
        # print 2
        child1 = parent1
        child2 = parent2
    # print len(child1), len(child2)

    return [child1, child2]


def negate(item):
    if item == "0":
        return "1"
    return "0"


# perform mutation
def mutation():

    chromosome1 = selected[0]
    chromosome2 = selected[1]
    # print chromosome1, chromosome2

    new1 = ""
    new2 = ""

    for i in range(0, total_items):
        p = numpy.random.binomial(1, mutation_rate)
        if p:
            new1 += negate(chromosome1[i])
        else:
            new1 += chromosome1[i]

    for i in range(0, total_items):
        p = numpy.random.binomial(1, mutation_rate)
        if p:
            new2 += negate(chromosome2[i])
        else:
            new2 += chromosome2[i]

    return [new1, new2]


def find_best(curr_best, best, b_volume):
    l = len(curr_benefits)
    item_index = -1

    for i in range(0, l):
        if best < curr_benefits[i]:
            best = curr_benefits[i]
            b_volume = curr_volumes[i]
            item_index = i

    if item_index == -1:
        return curr_best, best, b_volume

    return chromosomes[item_index], best, b_volume


def print_answer():
    print "Population size: ", population_size
    print "Crossover rate: ", crossover_rate
    print "Mutation rate: ", mutation_rate
    print "Stop after generations: ", limit
    print "The best solution is: ", best_benefits, "/", best_volumes
    print "Knapsack items: ",
    for i in range(0, total_items):
        if best_knapsack[i] == "1":
            stdout.write("%5d" % i)

    print ""


print "Number of items : ",
total_items = int(raw_input())
print "Enter capacity : ",
knapsack_capacity = int(raw_input())

b_range = 1000
v_range = 35

fitting = []
chromosomes = []
unique = {}

[benefits, volume, volume_sum] = generate_knapsack(total_items, b_range, v_range)

print_knapsack(total_items)

# create initial population
generate_chromosomes()

limit = 2000
population_size = total_items
generation = 0
crossover_rate = 0.95
mutation_rate = 0.05
curr_benefits = []
curr_volumes = []
best_benefits = 0
best_volumes = 0
best_knapsack = ""

while generation <= limit:
    del curr_benefits[:]
    del curr_volumes[:]
    fitness()
    [indices, selected] = select()
    result = crossover()
    # print result, indices
    result = mutation()
    # print len(result[0]), len(result[1]), result, indices
    chromosomes[indices[0]] = result[0]
    chromosomes[indices[1]] = result[1]

    best_knapsack, best_benefits, best_volumes = find_best(best_knapsack, best_benefits, best_volumes)

    generation += 1


print_answer()