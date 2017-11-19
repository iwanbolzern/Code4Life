import copy
from typing import List

from utils import sample_sort, get_next_molecule, positive_list_difference
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
    missing_molecules = positive_list_difference(player.storage, sample.cost)
    missing_molecules_sum = sum(missing_molecules)
    if missing_molecules_sum == 0:
        new_exp = copy.copy(player.expertise)
        new_exp[sample.exp.value] += 1
        project_diffs = (sum(positive_list_difference(proj.req_expertise, new_exp)) for proj in state.projects if not proj.completed)
        project_diffs = sum(project_diffs) * 0.10
        return 0.85 * (sample.health + expertise_weight) - project_diffs

    # missing molecules, but are available
    missing_molecules = positive_list_difference(state.available_molecules, sample.cost)
    missing_molecules_sum = sum(missing_molecules)
    if missing_molecules_sum == 0:
        new_exp = copy.copy(player.expertise)
        new_exp[sample.exp.value] += 1
        project_diffs = (sum(positive_list_difference(proj.req_expertise, new_exp)) for proj in state.projects if not proj.completed)
        project_diffs = sum(project_diffs) * 0.10
        return 0.5 * (sample.health + expertise_weight) - project_diffs

    # unproducible
    return 0.05 * (sample.health + expertise_weight)


def get_rank(state, player):
    total_ex = sum(player.expertise)
    if total_ex >= 9:
        return 3
    elif total_ex >= 2:
        return 2
    else:
        return 1

def possible_moves(state: State, player: Robot) -> List[Move]:
    pos_moves = []
    # start position
    if player.target == Location.START_POS:
        pos_moves.append(Move(Action.GOTO, Location.SAMPLES))

    # Sample position
    elif player.target == Location.SAMPLES:
        #TODO: check if we should allow to go to Molecules or Factory
        if len(player.samples) < 3:
            pos_moves.append(Move(Action.CONNECT, get_rank(state, player)))
        else:
            pos_moves.append(Move(Action.GOTO, Location.DIAGNOSIS))

    # Diagnosis Station TODO: check if this rules make sense
    elif player.target == Location.DIAGNOSIS:
        undiagnosed_samples = player.undiagnosed_samples
        diagnosed_samples = player.diagnosed_samples
        if undiagnosed_samples:
            pos_moves.append(Move(Action.CONNECT, undiagnosed_samples[0].id))
        elif len(diagnosed_samples) >= 3 and player.prev_location != Location.MOLECULES:
            pos_moves.append(Move(Action.GOTO, Location.MOLECULES))
        elif len(diagnosed_samples) < 3:
            pos_moves.append(Move(Action.GOTO, Location.SAMPLES))
            # take a sample from the cloud
            for s in state.cloud_samples:
                if Robot.could_satisfy(s.cost, state.available_molecules, player.storage, player.expertise):
                    id = sorted(state.cloud_samples, key=lambda x: sample_sort(x,player,state))[0].id
                    pos_moves.append(Move(Action.CONNECT, id))

        # drop worst sample into the cloud
        if diagnosed_samples:
            id = player.get_sorted_samples(state)[-1].id
            pos_moves.append(Move(Action.CONNECT, id))

        if player.ready_samples(state):
            pos_moves.append(Move(Action.GOTO, Location.LABORATORY))

    # Molecules Station
    elif player.target == Location.MOLECULES:
        missing_molecules = player.missing_molecules(state)
        missing_molecule = get_next_molecule(missing_molecules, state)
        if player.id == 0:
            pass#debug(missing_molecules)

        if sum(player.storage) < 10 and missing_molecule:
            pos_moves.append(Move(Action.CONNECT, missing_molecule))
        # move to other station
        ready_samples = player.ready_samples(state)
        if ready_samples:
            pos_moves.append(Move(Action.GOTO, Location.LABORATORY))
        elif len(player.samples) < 3:
            pos_moves.append(Move(Action.GOTO, Location.SAMPLES))
        else:
            pos_moves.append(Move(Action.GOTO, Location.DIAGNOSIS))
        # just wait
        # if player.score + sum(s.health for s in ready_samples) > \
        #     state.get_enemy(player).score + sum(s.health for s in state.get_enemy(player).ready_samples(state)):
        #     pos_moves.append(Move(Action.GOTO, Location.MOLECULES))

    elif player.target == Location.LABORATORY:
        ready_samples = player.ready_samples(state)
        if ready_samples:
            pos_moves.append(Move(Action.CONNECT, ready_samples[0].id))

            if player.score + sum(s.health for s in ready_samples) > \
            state.get_enemy(player).score + sum(s.health for s in state.get_enemy(player).ready_samples(state)) and \
                    state.get_enemy(player).target != Location.SAMPLES:
                pos_moves.append(Move(Action.GOTO, Location.LABORATORY))
        else:
            pos_moves.append(Move(Action.GOTO, Location.SAMPLES))
            if player.diagnosed_samples:
                pos_moves.append(Move(Action.GOTO, Location.MOLECULES))

            if state.cloud_samples:
                pos_moves.append(Move(Action.GOTO, Location.DIAGNOSIS))


    return pos_moves

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
