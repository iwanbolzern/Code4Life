import copy
import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
from enum import Enum

class Location(Enum):
    SAMPLES = 0
    DIAGNOSIS = 1
    MOLECULES = 2
    LABORATORY = 3
    START_POS = 4

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
        self.target = Location[target] #module where the player is
        self.eta = eta
        self.score = score
        self.storage = [int(storage_a), int(storage_b), int(storage_c), int(storage_d), int(storage_e)]
        self.expertise = [int(expertise_a), int(expertise_b), int(expertise_c), int(expertise_d), int(expertise_e)]

    @property
    def storage_size(self):
        return sum(self.storage)

    def satisfy(self, cost):
        collected_molecules = copy.deepcopy(self.storage)
        for m_type, cost in zip(range(len(cost)), cost):
            collected_molecules[m_type] -= cost
            if collected_molecules[m_type] < 0:
                return False
        return True

class State:

    def __init__(self):
        self.robot_a = None
        self.robot_b = None
        self.available = None
        self.samples = []

    @property
    def sample_robot_a(self):
        return [s for s in self.samples if s.carried_by == 0]

    @property
    def sample_robot_a_count(self):
        return len(self.sample_robot_a)

    @property
    def get_sample_id(self):
        # todo improve this
        return [s for s in self.samples if s.carried_by == -1][0].id

    @property
    def get_missing_molecule_id(self):
        collected_molecules = copy.deepcopy(self.robot_a.storage)
        for sample in state.sample_robot_a:
            for m_type, cost in zip(range(len(sample.cost)), sample.cost):
                collected_molecules[m_type] -= cost
                if collected_molecules[m_type] < 0:
                    return MoleculeType(m_type).name

        return None

def read_input():
    state = State()
    state.robot_a = Robot(*input().split())
    state.robot_b = Robot(*input().split())
    state.available = [int(i) for i in input().split()]

    sample_count = int(input())
    for i in range(sample_count):
        sample = Sample(*input().split())
        state.samples.append(sample)

    return state

def possible_moves(state, id):
    if state.robot_a.target == Location.START_POS:
        return 'GOTO DIAGNOSIS'
    elif state.robot_a.target == Location.SAMPLES:
        pass
    elif state.robot_a.target == Location.DIAGNOSIS:
        if state.sample_robot_a_count < 3:
            return 'CONNECT {}'.format(state.get_sample_id)
        else:
            return 'GOTO MOLECULES'
    elif state.robot_a.target == Location.MOLECULES:
        if state.robot_a.storage_size < 10 and state.get_missing_molecule_id:
            return 'CONNECT {}'.format(state.get_missing_molecule_id)
        else:
            return 'GOTO LABORATORY'
    elif state.robot_a.target == Location.LABORATORY:
        if state.sample_robot_a_count > 0 and\
            state.robot_a.satisfy(state.sample_robot_a[0].cost):
            return 'CONNECT {}'.format(state.sample_robot_a[0].id)
        else:
            return 'GOTO DIAGNOSIS'

# ignore this line for now
project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]

# game loop
while True:
    state = read_input()
    print(possible_moves(state, None))