import copy
from enum import Enum
from typing import List

from arena import Action
from main import State, Location


class Player(Enum):
    me = 0
    enemy = 1

class Move:

    def __init__(self, cmd: Action=None, arg=None):
        self.cmd: Action = cmd
        self.arg = arg

class Variation:

    def __init(self, score, moves):
        self.score = score
        self.moves = moves # array of pair of actions vector<array<action,2>> Moves;


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

def possible_moves(state, player) -> List[Move]:
    pos_moves = []
    # start position
    if state.robot_a.target == Location.START_POS:
        pos_moves.append(Move(Action.GOTO, Location.SAMPLES))

    # Sample position
    elif state.robot_a.target == Location.SAMPLES:
        #TODO: check if we should allow to go to Molecules or Factory
        if state.sample_robot_a_count < 3:
            pos_moves.append(Move(Action.CONNECT, get_rank(state, player)))
        else:
            return pos_moves.ap(Move(Action.GOTO, Location.DIAGNOSIS))

    # Diagnosis Station
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
        if state.sample_robot_a_count > 0 and \
                state.robot_a.satisfy(state.sample_robot_a[0].cost):
            return 'CONNECT {}'.format(state.sample_robot_a[0].id)
        else:
            return 'GOTO DIAGNOSIS'

    return pos_moves

def simulate_action(state, my_action, enemy_action) -> State:
    """ Returns new game state after both actions are performed
    :param state:
    :param my_action:
    :param enemy_action:
    """
    pass

def minimax(state, depth, max_depth, alpha, beta) -> Variation:
    if depth == max_depth:
        return Variation(eval(state), [])

    my_branch = possible_moves(state, Player.me)
    enemy_branch = possible_moves(state, Player.enemy)

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

    # action
    # Decide_Move(state)
    # {
    #     variation
    # best_var;
    # depth = 1;
    # while (depth <= 201 - turn){// Don't look past end of game
    # try{
    # best_var=Minimax(S, 0, depth, -inf, +inf); // Minimax throws an exception if time runs out
    # ++depth;
    # }
    # catch(...)
    # {
    # break;
    # }
    # }
    # return best_var.Moves[0][0];
    # }
# variation Minimax(state,depth,max_depth,alpha,beta){
#     if(depth==max_depth){
#         return variation{Eval(state),{}};
#     }
#     array<vector<action>,2> Branch={Possible_Moves(state,player0),Possible_Moves(state,player1)};
#     variation Best_var={-infinity,{}};
#     for(action mv:Branch[0]){
#         variation Best_var2{+infinity,{}};
#         local_beta=beta;
#         for(action mv2:Branch[1]){
#             state2=state;
#             SimulateActions(state2,{mv,mv2});
#             variation var=Minimax(state2,depth+1,max_depth,alpha,local_beta);
#             if(var.score<Best_var2.score){
#                 Best_var2=var;
#                 Best_var2.Moves.insert(at beginning,{mv,mv2});
#             }
#             local_beta=min(var.score,local_beta);
#             if(local_beta<=alpha){
#                 break;
#             }
#         }
#         if(Best_var2.score>Best_var.score){
#             Best_var=Best_var2;
#         }
#         alpha=max(alpha,Best_var2.score);
#         if(beta<=alpha){
#             break;
#         }
#     }
#     return Best_var;
# }