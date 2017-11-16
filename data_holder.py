from enum import Enum

import copy

import utils

class Action(Enum):
    GOTO = 0
    CONNECT = 1

class Move:

    def __init__(self, cmd: Action=None, arg=None):
        self.action: Action = cmd
        self.arg = arg

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
            satisfy, collected_molecules = Robot.satisfy(s.cost, collected_molecules, self.expertise)
            if satisfy:
                ready_samples.append(s)
        return ready_samples

    def get_sorted_samples(self, state: State):
        return self.diagnosed_samples.sort(key=lambda s: utils.sample_sort(s, self, state))

    @property
    def missing_molecules(self, state):
        missing_molecules = []
        for i, sample in zip(range(self.get_sorted_samples(state)), state.get_sorted_samples(state)):
            missing_molecules.append(copy.deepcopy(self.storage) if i == 0 else missing_molecules[i - 1])
            for m_type, cost in zip(range(len(sample.cost)), sample.cost):
                missing_molecules[i][m_type] -= cost
                if missing_molecules[i][m_type] < 0:
                    return MoleculeType(m_type).name

        return None

    @staticmethod
    def satisfy(cost, collected_molecules, expertise):
        for m_type, cost in zip(range(len(cost)), cost):
            collected_molecules[m_type] -= (cost-expertise[m_type])
            if collected_molecules[m_type] < 0:
                return False, collected_molecules
        return True, collected_molecules


class State:

    def __init__(self):
        self.robot_a = None
        self.robot_b = None
        self.available_molecules = None #[#a, #b...]
        self.cloud_samples = []
        self.projects = None

    def add_sample(self, s):
        if s.carried_by == -1:
            self.cloud_samples.append(s)
        elif s.carried_by == 0:
            self.robot_a.samples.append(s)
        else:
            self.robot_b.samples.append(s)

    def get_enemy(self, robot):
        return self.robot_a if robot == self.robot_b else self.robot_b