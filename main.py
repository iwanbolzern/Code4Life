import copy
import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
from enum import Enum

#SAMPLES	DIAGNOSIS	MOLECULES	LABORATORY  Start area
#SAMPLES	0	3	3	3   2
#DIAGNOSIS	3	0	3	4   2
#MOLECULES	3	3	0	3   2
#LABORATORY	3	4	3	0   2
#Start area	2	2	2	2   0
import utils

movement_matrix = [[0,3,3,3,2],
                   [3,0,3,4,2],
                   [3,3,0,3,2],
                   [3,4,3,0,2],
                   [2,2,2,2,0]]

def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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

class Project:

    def __init__(self, expertise):
        self.req_expertise = expertise

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
        self.samples = []

    @property
    def storage_size(self):
        return sum(self.storage)

    @property
    def undiagnosed_samples(self):
        return [s for s in self.samples if sum(s.cost) <= 0]

    @property
    def diagnosed_samples(self):
        return [s for s in self.samples if sum(s.cost) > 0]

    @property
    def ready_samples(self):
        ready_samples = []
        collected_molecules = copy.deepcopy(self.storage)
        for s in self.get_sorted_samples():
            satisfy, collected_molecules = Robot.satisfy(s.cost, collected_molecules)
            if satisfy:
                ready_samples.append(s)
        return ready_samples

    def get_sorted_samples(self, state: State):
        return self.diagnosed_samples.sort(key=lambda s: utils.sample_sort(s, self, state))

    @property
    def missing_molecules(self):
        missing_molecules = []
        for i, sample in zip(range(state.get_sorted_samples(state)), state.get_sorted_samples(state)):
            missing_molecules.append(copy.deepcopy(self.storage) if i == 0 else missing_molecules[i - 1])
            for m_type, cost in zip(range(len(sample.cost)), sample.cost):
                missing_molecules[i][m_type] -= cost
                if missing_molecules[i][m_type] < 0:
                    return MoleculeType(m_type).name

        return None

    @staticmethod
    def satisfy(cost, collected_molecules):
        for m_type, cost in zip(range(len(cost)), cost):
            collected_molecules[m_type] -= cost
            if collected_molecules[m_type] < 0:
                return False, collected_molecules
        return True, collected_molecules

class State:

    def __init__(self):
        self.robot_a = None
        self.robot_b = None
        self.available_molecules = None #[#a, #b...]
        self.cloud_samples = []

    def add_sample(self, s):
        if s.carried_by == -1:
            self.cloud_samples.append(s)
        elif s.carried_by == 0:
            self.robot_a.samples.append(s)
        else:
            self.robot_b.samples.append(s)

    @property
    def sample_robot_a(self):
        return self.robot_a.samples

    @property
    def sample_robot_a_count(self):
        return len(self.sample_robot_a)

    @property
    def undiagnosed_sample_robot_a(self):
        return [s for s in self.robot_a.samples if sum(s.cost) <= 0]

    @property
    def undiagnosed_sample_robot_a_count(self):
        return len(self.undiagnosed_sample_robot_a)

    @property
    def get_sample_id(self):
        # todo improve this
        return self.sample_robot_a[0].id

    @property
    def get_rank(self):
        total_ex = sum(self.robot_a.expertise)
        if total_ex >= 12:
            return 3
        elif total_ex >= 9:
            return 2
        else:
            return 1

    def get_enemy(self, robot):
        return self.robot_a if robot == self.robot_b else self.robot_b

def read_input():
    state = State()
    state.robot_a = Robot(*input().split())
    state.robot_b = Robot(*input().split())
    state.available = [int(i) for i in input().split()]

    sample_count = int(input())
    for i in range(sample_count):
        sample = Sample(*input().split())
        state.add_sample(sample)

    return state

def possible_moves(state, id):
    if state.robot_a.target == Location.START_POS:
        return 'GOTO SAMPLES'
    elif state.robot_a.target == Location.SAMPLES:
        if state.sample_robot_a_count < 3:
            return 'CONNECT {}'.format(state.get_rank)
        else:
            return 'GOTO DIAGNOSIS'
    elif state.robot_a.target == Location.DIAGNOSIS:
        if state.undiagnosed_sample_robot_a_count > 0:
            return 'CONNECT {}'.format(state.undiagnosed_sample_robot_a[0].id)
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

projects = []
project_count = int(input())
for i in range(project_count):
    #a, b, c, d, e = [int(j) for j in input().split()]
    project = Project([int(j) for j in input().split()])
    projects.append(project)

# game loop
while True:
    state = read_input()
    print(possible_moves(state, None))