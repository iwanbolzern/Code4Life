import copy
from data_holder import State, Move
from simulation_data import get_sample
from minimax import get_missing_molecules
from utils import positive_list_difference

#SAMPLES	DIAGNOSIS	MOLECULES	LABORATORY  Start area
#SAMPLES	0	3	3	3   2
#DIAGNOSIS	3	0	3	4   2
#MOLECULES	3	3	0	3   2
#LABORATORY	3	4	3	0   2
#Start area	2	2	2	2   0
from data_holder import Robot, Action, Location

movement_matrix = [[0,3,3,3,2],
                   [3,0,3,4,2],
                   [3,3,0,3,2],
                   [3,4,3,0,2],
                   [2,2,2,2,0]]

def simulate_action(state: State, my_action: Move, enemy_action: Move):
    """ Returns new game state after both actions are performed
    :param state:
    :param my_action:
    :param enemy_action:
    """

    simulate_player(state, state.robot_a, my_action)
    simulate_player(state, state.robot_b, enemy_action)

def simulate_player(state: State, player: Robot, move: Move):
    if player.eta == 0:
        if move.action == Action.GOTO:
            player.eta = movement_matrix[player.target.value][move.arg.value]
            player.target = move.arg

        elif move.action == Action.CONNECT:
            if player.target == Location.SAMPLES and move.arg in [1,2,3]:
                sample = get_sample(move.arg)
                sample.carried_by = player.id
                state.add_sample(sample)

            elif player.target == Location.MOLECULES and move.arg in [1,2,3,4,5]:
                if state.available_molecules[move.arg] <= 0:
                    raise "Molecule " + move.arg + " not available"

                state.available_molecules[move.arg] -= 1
                player.storage[move.arg] += 1

            elif player.target == Location.LABORATORY:
                samples = list(filter(lambda s: s.id == move.arg, player.samples))
                if len(samples) == 0:
                    raise "Invalid sample " + move.arg

                sample = samples[0]
                # difference = positive_list_difference(player.storage, sample.cost)
                # if sum(difference) > 0:
                #    raise "Molecules not available for " + move.arg

                player.storage = list(map(int.__sub__, player.storage, sample.cost))
                player.score += sample.health
                player.expertise[sample.exp.value] += 1
                state.remove_sample(sample)

            elif player.target == Location.DIAGNOSIS:
                player_samples = list(filter(lambda s: s.id == move.arg, player.samples))
                cloud_samples = list(filter(lambda s: s.id == move.arg, state.cloud_samples))
                if len(player_samples) == 1:
                    sample = player_samples[0]
                    if sample.diagnosed:
                        state.remove_sample(sample)
                        sample.carried_by = -1
                        state.add_sample(sample)
                    else:
                        sample.cost = sample.cost_tmp

                elif len(cloud_samples) == 1:
                    sample = cloud_samples[0]
                    if len(player.samples) < 3:
                        state.remove_sample(sample)
                        sample.carried_by = player.id
                        state.add_sample(sample)

                if len(player_samples) == 0 and len(cloud_samples) == 0:
                    debug([s.id for s in player_samples])
                    debug([s.id for s in cloud_samples])
                    raise Exception("Invalid sample " + str(move.arg))

    player.eta = max(0, player.eta - 1)
    for project in state.projects:
        if not project.completed:
            difference = positive_list_difference(player.expertise, project.req_expertise)
            if sum(difference) == 0:
                player.score += 50
                project.completed = True
