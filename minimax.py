import copy
from enum import Enum


class Player(Enum):
    me = 0
    enemy = 1

class Variation:

    def __init(self, score, moves):
        self.score = score
        self.moves = moves # array of pair of actions vector<array<action,2>> Moves;


def eval(state):
    pass

def possible_moves(state, player):
    pass

def simulate_action(state, my_action, enemy_action):
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