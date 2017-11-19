import copy
from typing import List, Iterator

from data_holder import Sample, State, Move, Action, MoleculeType, Project, Robot
from minimax import eval_sample


def sample_sort(sample: Sample, player, state: State):
    return eval_sample(state, player, sample)

def list_difference(left: List[int], right: List[int]) -> Iterator[int]:
    return map(int.__sub__, left, right)

def positive_list_difference(left: List[int], right: List[int]) -> Iterator[int]:
    return [0 if d < 0 else d for d in list_difference(left, right)]

def get_next_molecule(missing_molecules, state):
    for missing_per_sample in missing_molecules:
        for type, missing_count in enumerate(missing_per_sample):
            if missing_count < 0 and state.available_molecules[type] > 0:
                return MoleculeType(type)
    return None

def sample_helps_projects(sample: Sample, player: Robot, projects: List[Project]):
    count = 0
    for project in projects:
        # expertise is not in project
        if project.req_expertise[sample.exp.value] == 0:
            continue

        # project expertise is larger than player expertise
        if project.req_expertise[sample.exp.value] > player.expertise[sample.exp.value]:
            count += 1

    return count

def move_to_string(move: Move):
    if move.action == Action.GOTO:
        return '{} {}'.format(move.action.name, move.arg.name)
    elif move.action == Action.CONNECT:
        if isinstance(move.arg, MoleculeType):
            return '{} {}'.format(move.action.name, move.arg.name)
        elif isinstance(move.arg, Sample):
            return '{} {}'.format(move.action.name, move.arg.id)
        else:
            return '{} {}'.format(move.action.name, move.arg)
