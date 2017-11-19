import copy
from typing import List

from utils import sample_sort, get_next_molecule, positive_list_difference, sample_helps_projects
from data_holder import State, Robot, Location, Action, Move, Sample
from simulation import simulate_action

expertise_weight = 10

class Variation:
    def __init__(self, score, moves):
        self.score = score
        self.moves = moves

def eval(state: State):
    return eval_robot(state, state.robot_a) - eval_robot(state,state.robot_b)

def eval_robot(state: State, player: Robot):
    eval_score = player.score
    eval_score += expertise_weight * sum(player.expertise)

    sample_scores = [eval_sample(state, player, s) for s in player.samples]

    return eval_score + sum(sample_scores)

def eval_sample(state: State, player: Robot, sample: Sample):
    min_score = 1 # rank 1 min score
    if sample.rank == 2:
        min_score = 10
    if sample.rank == 3:
        min_score = 30

    # sample is undiagnosed
    sample_cost = sum(sample.cost)
    if sample_cost <= 0:
        return 0.15 * (min_score + expertise_weight)

    # sample is diagnosed but unknown (simulated)
    if sample_cost <= 0 and sum(sample.cost_tmp) > 0:
        return 0.175 * (min_score + expertise_weight)

    # sample is ready for LABORATORY
    sample_cost_exp = positive_list_difference(sample.cost, player.expertise)

    # balance expertise gain by choosing samples which contribute to currently low sample expertise
    max_sample_expertise = max(player.expertise)
    sample_exp_balance_factor = max_sample_expertise - player.expertise[sample.exp.value]

    missing_molecules = positive_list_difference(player.storage, sample_cost_exp)
    missing_molecules_sum = sum(missing_molecules)
    if missing_molecules_sum == 0:
        helps_projects = sample_helps_projects(sample, player, state.projects)
        return 0.85 * (sample.health + expertise_weight) + (-0.5 if not helps_projects and sample.rank == 1 else helps_projects) + sample_exp_balance_factor

    # missing molecules, but are available
    sample_cost_exp = positive_list_difference(sample.cost, player.expertise)

    missing_molecules = positive_list_difference(state.available_molecules, sample_cost_exp)
    missing_molecules_sum = sum(missing_molecules)

    molecule_difference = positive_list_difference(sample_cost_exp, player.storage)
    molecule_difference_sum = sum(molecule_difference)
    player_storage_sum = sum(player.storage)

    if missing_molecules_sum == 0 and molecule_difference_sum + player_storage_sum <= 10:
        helps_projects = sample_helps_projects(sample, player, state.projects)
        return 0.5 * (sample.health + expertise_weight) + (-0.5 if not helps_projects and sample.rank == 1 else helps_projects) + sample_exp_balance_factor

    # unproducible
    return 0.05 * (sample.health + expertise_weight)


def get_rank(state, player):
    # num_rank_1 = len([s for s in player.samples if s.rank == 1])
    num_rank_3 = len([s for s in player.samples if s.rank == 3])
    total_ex = sum(player.expertise)
    if total_ex >= 12:
        if num_rank_3 == 2:
            return 2
        return 3
    elif total_ex >= 7:
        # if num_rank_1 <= 1:
            # return 1
        return 2
    else:
        return 1


def producible_cloud_samples(player, state):
    samples = []
    for s in state.cloud_samples:
        helps_projects = sample_helps_projects(s, player, state.projects)
        if helps_projects >= 1 and Robot.could_satisfy(s.cost, state.available_molecules, player.storage, player.expertise):
            samples.append(s)
    return sorted(samples, key=lambda s: sample_sort(s, player, state))

def producible_samples_in_hand(player, state):
    samples = []
    for s in player.diagnosed_samples:
        if Robot.could_satisfy(s.cost, state.available_molecules, player.storage, player.expertise):
            samples.append(s)
    return samples

def not_useful_samples_in_hand(player, state):
    samples = []
    for s in player.diagnosed_samples:
        if s.health < 10:
            helps_projects = sample_helps_projects(s, player, state.projects)
            if helps_projects <= 0:
                samples.append(s)
    return samples


def possible_move(state: State, player: Robot) -> Move:
    # start position
    if player.target == Location.START_POS:
        return Move(Action.GOTO, Location.SAMPLES)

    # Sample position
    elif player.target == Location.SAMPLES:
        if len(player.samples) < 3:
            return Move(Action.CONNECT, get_rank(state, player))

        prod_samples_in_hand = producible_samples_in_hand(player, state)
        if len([s for s in prod_samples_in_hand if s.rank == 1]) > 1 \
                or [s for s in prod_samples_in_hand if s.rank > 1]:
            return Move(Action.GOTO, Location.MOLECULES)

        return Move(Action.GOTO, Location.DIAGNOSIS)

    # Diagnosis Station TODO: check if this rules make sense
    elif player.target == Location.DIAGNOSIS:
        undiagnosed_samples = player.undiagnosed_samples
        diagnosed_samples = player.diagnosed_samples
        if undiagnosed_samples:
            return Move(Action.CONNECT, undiagnosed_samples[0].id)

        producible_in_hand = producible_samples_in_hand(player, state)
        if (len([s for s in player.ready_samples(state) if s.rank == 1]) >= 2 or \
                [s for s in player.ready_samples(state) if s.rank > 1]) and not \
                producible_in_hand:
            return Move(Action.GOTO, Location.LABORATORY)

        if producible_in_hand and player.prev_location != Location.MOLECULES:
            return Move(Action.GOTO, Location.MOLECULES)

        producible_in_cloud = producible_cloud_samples(player, state)
        not_useful_samples = not_useful_samples_in_hand(player, state)

        if not_useful_samples:
            return Move(Action.CONNECT, not_useful_samples[0].id)

        if producible_in_cloud and len(player.samples) >= 3:
            id = player.get_sorted_samples(state)[-1].id
            return Move(Action.CONNECT, id)

        if producible_in_cloud:
            return Move(Action.CONNECT, producible_in_cloud[0].id)

        if len(diagnosed_samples) < 3:
            return Move(Action.GOTO, Location.SAMPLES)

        # drop worst sample into the cloud
        # if len(diagnosed_samples) >= 3 and not producible and not producible_in_hand:
        id = player.get_sorted_samples(state)[-1].id
        return Move(Action.CONNECT, id)

    # Molecules Station
    elif player.target == Location.MOLECULES:
        missing_molecules = player.missing_molecules(state)
        missing_molecule = get_next_molecule(missing_molecules, state)

        if sum(player.storage) < 10 and missing_molecule:
            return Move(Action.CONNECT, missing_molecule)

        # move to other station
        ready_samples = player.ready_samples(state)
        if ready_samples:
            return Move(Action.GOTO, Location.LABORATORY)

        if producible_cloud_samples(player, state) or len(player.samples) >= 3:
            return Move(Action.GOTO, Location.DIAGNOSIS)

        return Move(Action.GOTO, Location.SAMPLES)

        # just wait
        # if player.score + sum(s.health for s in ready_samples) > \
        #     state.get_enemy(player).score + sum(s.health for s in state.get_enemy(player).ready_samples(state)):
        #     return Move(Action.GOTO, Location.MOLECULES)

    elif player.target == Location.LABORATORY:
        ready_samples = player.ready_samples(state)
        if ready_samples:
            return Move(Action.CONNECT, ready_samples[0].id)

            # if player.score + sum(s.health for s in ready_samples) > \
            # state.get_enemy(player).score + sum(s.health for s in state.get_enemy(player).ready_samples(state)) and \
            #         state.get_enemy(player).target != Location.SAMPLES:
            #     return Move(Action.GOTO, Location.LABORATORY)

        if len([s for s in producible_samples_in_hand(player, state) if s.rank == 1]) >= 2 \
                or len([s for s in producible_samples_in_hand(player, state) if s.rank > 1]) >= 2 :
            return Move(Action.GOTO, Location.MOLECULES)
        elif [s for s in producible_cloud_samples(player, state) if s.rank >= 2]:
             return Move(Action.GOTO, Location.DIAGNOSIS)

        return Move(Action.GOTO, Location.SAMPLES)

    return Move(Action.GOTO, Location.SAMPLES)

def minimax(state, depth, max_depth, alpha, beta) -> Variation:
    if depth == max_depth:
        return Variation(eval(state), [])

    my_branch = possible_moves(state, state.robot_a)
    enemy_branch = possible_moves(state, state.robot_b)

    best_variation = Variation(float('-inf'), []) #float just bc there is no int('-inf')
    for my_action in my_branch:
        best_variation2 = Variation(float('inf'), [])
        local_beta = beta
        for en_action in enemy_branch:
            tmp_state = copy.deepcopy(state)
            simulate_action(tmp_state, my_action, en_action)
            local_variation = minimax(tmp_state, depth+1, max_depth, alpha, local_beta)
            if local_variation.score < best_variation2.score:
                best_variation2 = local_variation
                best_variation2.moves = [[my_action, en_action]] + best_variation2.moves
            local_beta = min(local_variation.score, local_beta)
            if local_beta <= alpha:
                break
        if best_variation2.score > best_variation.score:
            best_variation = best_variation2

        alpha = max(alpha, best_variation2.score)
        if beta <= alpha:
            break

    return best_variation
