import copy
from enum import Enum
from typing import List

import utils
from data_holder import State, Robot, Location, Action, Move
from simulation import simulate_action

class Variation:

    def __init(self, score, moves):
        self.score = score
        self.moves = moves

def eval(state):
    pass

def get_rank(state, player):
    total_ex = sum(player.expertise)
    if total_ex >= 12:
        return 3
    elif total_ex >= 9:
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
            return pos_moves.ap(Move(Action.GOTO, Location.DIAGNOSIS))

    # Diagnosis Station TODO: check if this rules make sense
    elif player.target == Location.DIAGNOSIS:
        if player.undiagnosed_samples:
            pos_moves.append(Move(Action.CONNECT, player.undiagnosed_samples[0]))
        elif len(player.diagnosed_samples) >= 3:
            pos_moves.append(Move(Action.GOTO, Location.MOLECULES))
        elif len(player.diagnosed_samples) < 3:
            pos_moves.append(Move(Action.GOTO, Location.SAMPLES))
            # take a sample from the cloud
            if state.cloud_samples:
                id = state.cloud_samples.sort(key=lambda x: utils.sample_sort())[0].id
                pos_moves.append(Move(Action.CONNECT, id))

        # drop worst sample into the cloud
        if player.diagnosed_samples:
            id = player.get_sorted_samples(state)[-1]
            pos_moves.append(Move(Action.CONNECT, id))

        if player.ready_samples:
            pos_moves.append(Move(Action.GOTO, Location.LABORATORY))
    # Molecules Station
    elif player.target == Location.MOLECULES:
        missing_molecule = utils.get_next_molecule(player.missing_molecules, state)
        if sum(player.storage) < 10 and missing_molecule:
            pos_moves.append(Move(Action.CONNECT, missing_molecule))
        # move to other station
        if player.ready_samples:
            pos_moves.append(Move(Action.GOTO, Location.LABORATORY))
        elif len(player.samples) < 3:
            pos_moves.append(Move(Action.GOTO, Location.SAMPLES))
        else:
            pos_moves.append(Move(Action.GOTO, Location.DIAGNOSIS))
        # just wait
        if player.score + sum(player.ready_samples, key=lambda s: s.cost) > \
            state.get_enemy(player).score + sum(state.get_enemy(player).ready_samples, key=lambda s: s.cost):
            pos_moves.append(Move(Action.GOTO, Location.MOLECULES))

    elif player.target == Location.LABORATORY:
        if player.ready_samples:
            pos_moves.append(Move(Action.CONNECT, player.ready_samples[0]))

            if player.score + sum(player.ready_samples, key=lambda s: s.cost) > \
            state.get_enemy(player).score + sum(state.get_enemy(player).ready_samples, key=lambda s: s.cost) and \
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
            if local_variation.score < best_variation2:
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
