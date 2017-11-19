import copy
import sys
from threading import Timer, Thread, Event
import time
from datetime import datetime

from minimax import Variation, minimax, possible_move
from utils import move_to_string
from data_holder import State, Robot, Sample, Project, Location, Action, Move


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()


#init game
projects = []
input_t = input()
debug(input_t)
project_count = int(input_t)
for i in range(project_count):
    #a, b, c, d, e = [int(j) for j in input().split()]
    input_t = input()
    debug(input_t)
    project = Project([int(j) for j in input_t.split()])
    projects.append(project)

state = None
prev_robot_a = None
prev_robot_b = None
same_station_count_a = 0
same_station_count_b = 0

def read_input():
    time = datetime.now()
    global state
    global prev_robot_a
    global prev_robot_b
    global same_station_count_a
    global same_station_count_b
    state = State()

    #Read robot a
    input_t = input()
    debug(input_t)
    state.robot_a = Robot(0, *input_t.split())

    #Read robot b
    input_t = input()
    debug(input_t)
    state.robot_b = Robot(1, *input_t.split())

    state.robot_a.prev_location = prev_robot_a
    # add prev loctions
    if state.robot_a.eta <= 0:
        if prev_robot_a == state.robot_a.target:
            same_station_count_a += 1
        else:
            same_station_count_a = 0
        state.same_station_count_a = same_station_count_a
        prev_robot_a = state.robot_a.target


    state.robot_b.prev_location = prev_robot_b
    if state.robot_b.eta <= 0:
        if prev_robot_b == state.robot_b.target:
            same_station_count_b += 1
        else:
            same_station_count_b = 0
        state.same_station_count_b = same_station_count_b
        prev_robot_b = state.robot_b.target

    input_t = input()
    debug(input_t)
    state.available_molecules = [int(i) for i in input_t.split()]
    state.projects = projects

    input_t = input()
    debug(input_t)
    sample_count = int(input_t)
    for i in range(sample_count):
        input_t = input()
        debug(input_t)
        sample = Sample.from_input(*input_t.split())
        state.add_sample(sample)

    debug(datetime.now() - time)
    return state


best_move: Move = None
compute_thread = None
stop_event = None
timer = None


def decide_move(state: State):
    # depth = 3
    # while depth <= 3:
    #     best_var_tmp = minimax(state, 0, depth, float('-inf'), float('inf'))
    #     global best_var
    #     best_var = best_var_tmp
    #     depth += 1
    global best_move
    best_move = possible_move(state, state.robot_a)
    print_move()


def compute():
    state = read_input()
    debug(state)
    decide_move(state)


def print_move():
    if best_move:
        print(move_to_string(best_move))
    else:
        #You're fucked up. Go home and cry
        print(move_to_string(Move(Action.GOTO, Location.SAMPLES)))


turn = 1
# game loop
while True:
    s = time.time()
    compute()
    print(time.time() - s, file=sys.stderr)
