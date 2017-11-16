from data_holder import State, Move

#SAMPLES	DIAGNOSIS	MOLECULES	LABORATORY  Start area
#SAMPLES	0	3	3	3   2
#DIAGNOSIS	3	0	3	4   2
#MOLECULES	3	3	0	3   2
#LABORATORY	3	4	3	0   2
#Start area	2	2	2	2   0
movement_matrix = [[0,3,3,3,2],
                   [3,0,3,4,2],
                   [3,3,0,3,2],
                   [3,4,3,0,2],
                   [2,2,2,2,0]]

def simulate_action(state: State, my_action: Move, enemy_action: Move) -> State:
    """ Returns new game state after both actions are performed
    :param state:
    :param my_action:
    :param enemy_action:
    """
    pass