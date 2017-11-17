import copy
from enum import Enum

from utils import list_difference, sample_sort


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
        self.completed = False


class Sample:

    @staticmethod
    def from_input(sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e):
        sample = Sample([int(cost_a), int(cost_b), int(cost_c), int(cost_d), int(cost_e)], health, expertise_gain)
        sample.id = int(sample_id)
        sample.carried_by = int(carried_by)
        sample.rank = int(rank)
        sample.cost = sample.cost_tmp
        return sample

    def __init__(self, cost, health, exp):
        """ This is for a simulated sample
        :param cost:
        :param health:
        :param exp:
        """
        self.health = int(health)
        self.exp = MoleculeType[exp] if exp != '0' else None
        self.cost_tmp = cost
        self.cost = [0] * 5

    @property
    def diagnosed(self):
        return sum(self.cost) > 0


class State:

    def __init__(self):
        self.robot_a = None
        self.robot_b = None
        self.available_molecules = None #[#a, #b...]
        self.cloud_samples = []
        self.projects = []

    def add_sample(self, s):
        if s.carried_by == -1:
            self.cloud_samples.append(s)
        elif s.carried_by == 0:
            self.robot_a.samples.append(s)
        else:
            self.robot_b.samples.append(s)

    def remove_sample(self, s):
        if s.carried_by == -1:
            self.cloud_samples.remove(s)
        elif s.carried_by == 0:
            self.robot_a.samples.remove(s)
        else:
            self.robot_b.samples.remove(s)

    def get_enemy(self, robot):
        return self.robot_a if robot == self.robot_b else self.robot_b

class Robot:

    def __init__(self, id, target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e):
        self.id = id
        self.target = Location[target] #module where the player is
        self.eta = int(eta)
        self.score = int(score)
        self.storage = [int(storage_a), int(storage_b), int(storage_c), int(storage_d), int(storage_e)]
        self.expertise = [int(expertise_a), int(expertise_b), int(expertise_c), int(expertise_d), int(expertise_e)]
        self.samples = []

    @property
    def undiagnosed_samples(self):
        return [s for s in self.samples if sum(s.cost) <= 0]

    @property
    def diagnosed_samples(self):
        return [s for s in self.samples if sum(s.cost) > 0]

    def ready_samples(self, state):
        ready_samples = []
        collected_molecules = copy.deepcopy(self.storage)
        for s in self.get_sorted_samples(state):
            satisfy, collected_molecules = Robot.satisfy(s.cost, collected_molecules, self.expertise)
            if satisfy:
                ready_samples.append(s)
        return ready_samples

    def get_sorted_samples(self, state: State):
        return sorted(self.diagnosed_samples, key=lambda s: sample_sort(s, self, state))

    def missing_molecules(self, state):
        missing_molecules = []
        storage = copy.deepcopy(self.storage)
        sorted_samples = self.get_sorted_samples(state)
        for i, sample in enumerate(sorted_samples):
            missing_molecules.append(storage if i == 0 else missing_molecules[i - 1])
            missing_molecules[i] = list_difference(missing_molecules[i], sample.cost)

        return missing_molecules

    @staticmethod
    def satisfy(cost, collected_molecules, expertise):
        for m_type, cost in zip(range(len(cost)), cost):
            collected_molecules[m_type] -= (cost-expertise[m_type])
            if collected_molecules[m_type] < 0:
                return False, collected_molecules
        return True, collected_molecules

