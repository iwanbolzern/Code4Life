import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
from enum import Enum

class Location(Enum):
    SAMPLES = 0
    DIAGNOSIS = 1
    MOLECULES = 2
    LABORATORY = 3
    START = 4

class MoleculeType(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4

class Sample:

    def __init__(self, sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e):
        self.id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.cost = [int(cost_a), int(cost_b), int(cost_c), int(cost_d), int(cost_e)]

class Robot:

    def __init__(self, target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e):
        self.target = target
        self.eta = eta
        self.score = score
        self.storage = [int(storage_a), int(storage_b), int(storage_c), int(storage_d), int(storage_e)]
        self.expertise = [int(expertise_a), int(expertise_b), int(expertise_c), int(expertise_d), int(expertise_e)]

# ignore this line for now
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]

# game loop
while True:
    player_a = Robot(input().split())
    player_b = Robot(input().split())


    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    sample_count = int(input())
    samples = []
    for i in range(sample_count):
        sample = Sample(input().split())
        samples.append(sample)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print("GOTO DIAGNOSIS")