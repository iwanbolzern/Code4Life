import copy
import sys
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
    state.available = [int(i) for i in input().split()]
    state.projects = copy.deepcopy(projects)

    sample_count = int(input())
    for i in range(sample_count):
        sample = Sample(*input().split())
        state.add_sample(sample)

    return state


best_var: Variation = None
compute_thread = None
stop_event = None
timer = None


def decide_move(state: State):
    depth = 1
    while depth <= 401 - turn:
        best_var_tmp = minimax(state, 0, depth, float('-inf'), float('inf'))
        if stop_event.is_set(): # to make sure no old threads will post values
            break
        global best_var
        best_var = best_var_tmp
        depth += 1


def compute():
    state = read_input()
    decide_move(state)


def print_move():
    if best_var:
        print(utils.move_to_string(best_var.moves[0]))
    else:
        #You're fucked up. Go home and cry
        print(utils.move_to_string(Move(Action.GOTO, Location.SAMPLES)))

    stop_event.set()


turn = 1
# game loop
while True:
    timer = Timer(40 / 1000, print_move)
    timer.start()  # after 30 seconds, "hello, world" will be printed

    stop_event = Event()
    compute_thread = Thread(target=compute,  args=(stop_event, ))
    compute_thread.start()

