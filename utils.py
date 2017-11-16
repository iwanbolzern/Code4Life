from typing import List

from data_holder import Move, Action, MoleculeType
from main import Sample, State


def sample_sort(sample: Sample, player, state: State):
    pass
# TODO: implement this rule
# (MoleculesAvailable & & EnoughSpaceToTake ? 100: MoleculesAvailable? 1: 0)-MissingMolecules * 1e-3:


def get_next_molecule(missing_molecules: List[List[int]], state: State):
    for missing_per_sample in missing_molecules:
        for type, missing_count in zip(range(len(missing_per_sample)), missing_per_sample):
            if missing_count < 0 and state.available_molecules[type] > 0:
                return type
    return None

def move_to_string(move: Move):
    if move.action == Action.GOTO:
        return '{} {}'.format(move.action.name, move.arg.name)
    elif move.action == Action.CONNECT:
        if isinstance(move.arg, MoleculeType):
            return '{} {}'.format(move.action.name, move.arg.name)
        else:
            return '{} {}'.format(move.action.name, move.arg)
