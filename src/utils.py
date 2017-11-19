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
        enemy = state.robot_b
        enemy_samples = enemy.samples
        enemy_missing_molecules_sample_costs = []
        for enemy_sample in enemy_samples:
            enemy_missing_molecules_sample = positive_list_difference(enemy_sample.cost, enemy.expertise)
            enemy_missing_molecules_sample = positive_list_difference(enemy_missing_molecules_sample, enemy.storage)
            enemy_missing_molecules_sample_costs.append(enemy_missing_molecules_sample)

        # sum same molecules over all samples the enemy has in hand
        enemy_missing_molecules = [sum(x) for x in zip(*enemy_missing_molecules_sample_costs)]
        enemy_missing_molecules = enemy_missing_molecules if enemy_missing_molecules else (5 * [0])

        available_with_enemy_taken = [x - y for x, y in zip(state.available_molecules, enemy_missing_molecules)]
        for_us = [x - y for x, y in zip(available_with_enemy_taken, missing_per_sample)]

        should_take = [(type, missing_count) for type, missing_count in enumerate(for_us)]
        should_take = sorted(should_take, key=lambda x: x[1] * -1)

        debug('missing per sample', missing_per_sample)
        debug('should take ', should_take)


        for take in should_take:
            if missing_per_sample[take[0]] < 0 and state.available_molecules[take[0]] > 0 and \
                                    state.available_molecules[take[0]] + missing_per_sample[take[0]] >= 0:
                return MoleculeType(take[0])
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
