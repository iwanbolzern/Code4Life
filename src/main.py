import copy
import sys
import time
from threading import Timer, Thread, Event

from minimax import Variation, minimax
from utils import move_to_string
from data_holder import State, Robot, Sample, Project, Location, Action, Move


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


#init game
projects = []
project_count = int(input())
for i in range(project_count):
    #a, b, c, d, e = [int(j) for j in input().split()]
    project = Project([int(j) for j in input().split()])
    projects.append(project)


def read_input():
    state = State()
    state.robot_a = Robot(0, *input().split())
    state.robot_b = Robot(1, *input().split())
    state.available_molecules = [int(i) for i in input().split()]
    state.projects = copy.deepcopy(projects)

    sample_count = int(input())
    for i in range(sample_count):
        sample = Sample.from_input(*input().split())
        state.add_sample(sample)

    return state


best_var: Variation = None
compute_thread = None
stop_event = None
timer = None


def decide_move(state: State):
    depth = 6
    while depth <= 6:
        best_var_tmp = minimax(state, 0, depth, float('-inf'), float('inf'))
        global best_var
        best_var = best_var_tmp
        depth += 1
    print_move()


def compute():
    state = read_input()
    debug(state)
    decide_move(state)


def print_move():
    if best_var:
        print(move_to_string(best_var.moves[0][0]))
    else:
        #You're fucked up. Go home and cry
        print(move_to_string(Move(Action.GOTO, Location.SAMPLES)))


turn = 1
# game loop
while True:
    s = time.time()
    compute()
    print(time.time() - s, file=sys.stderr)
