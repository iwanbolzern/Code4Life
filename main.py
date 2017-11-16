import copy
import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
from enum import Enum
import utils

#SAMPLES	DIAGNOSIS	MOLECULES	LABORATORY  Start area
#SAMPLES	0	3	3	3   2
#DIAGNOSIS	3	0	3	4   2
#MOLECULES	3	3	0	3   2
#LABORATORY	3	4	3	0   2
#Start area	2	2	2	2   0
from data_holder import State, Robot, Sample, Project

movement_matrix = [[0,3,3,3,2],
                   [3,0,3,4,2],
                   [3,3,0,3,2],
                   [3,4,3,0,2],
                   [2,2,2,2,0]]

def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_input():
    state = State()
    state.robot_a = Robot(*input().split())
    state.robot_b = Robot(*input().split())
    state.available = [int(i) for i in input().split()]

    sample_count = int(input())
    for i in range(sample_count):
        sample = Sample(*input().split())
        state.add_sample(sample)

    return state


projects = []
project_count = int(input())
for i in range(project_count):
    #a, b, c, d, e = [int(j) for j in input().split()]
    project = Project([int(j) for j in input().split()])
    projects.append(project)

# game loop
while True:
    state = read_input()
    