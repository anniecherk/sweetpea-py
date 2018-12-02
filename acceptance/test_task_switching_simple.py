import operator as op
import pytest

from itertools import repeat

from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition
from sweetpea.constraints import NoMoreThanKInARow
from sweetpea import fully_cross_block, print_experiments, synthesize_trials_non_uniform, print_encoding_diagram, __generate_cnf


# Simple Factors
color  = Factor("color",  ["red", "blue"])
motion = Factor("motion", ["up", "down"])
task   = Factor("task",   ["color", "motion"])

# Response Definition
def response_left(task, color, motion):
    return (task == "color"  and color  == "red") or \
           (task == "motion" and motion == "up")

def response_right(task, color, motion):
    return not response_left(task, color, motion)

response = Factor("response", [
    DerivedLevel("left",  WithinTrial(response_left,  [task, color, motion])),
    DerivedLevel("right", WithinTrial(response_right, [task, color, motion]))
])

# Congruency Definition
def color_motion_congruent(color, motion):
    return ((color == "red") and (motion == "up")) or \
           ((color == "blue") and (motion == "down"))

def color_motion_incongruent(color, motion):
    return not color_motion_congruent(color, motion)

congruency = Factor("congruency", [
    DerivedLevel("con", WithinTrial(color_motion_congruent,   [color, motion])),
    DerivedLevel("inc", WithinTrial(color_motion_incongruent, [color, motion]))
])

# Task Transition
task_transition = Factor("task transition", [
    DerivedLevel("repeat", Transition(op.eq, [task, task])),
    DerivedLevel("switch", Transition(op.ne, [task, task]))
])

# Response Transition
response_transition = Factor("response transition", [
    DerivedLevel("repeat", Transition(op.eq, [response, response])),
    DerivedLevel("switch", Transition(op.ne, [response, response]))
])


def __assert_constraint():
    pass


def test_correct_solution_count():
    design =   [color, motion, task, response, congruency, task_transition, response_transition]
    crossing = [color, motion, task]

    k = 4
    constraints = [
        NoMoreThanKInARow(k, task_transition),
        NoMoreThanKInARow(k, response_transition)
    ]

    block = fully_cross_block(design, crossing, constraints)

    experiments = synthesize_trials_non_uniform(block, 100)

    assert len(experiments) == 100
    for e in experiments:
        print(str(e))
        assert list(repeat('repeat', 3)) not in [e['task transition'][i:i+3] for i in range(len(e['task transition']) - 3)]
        assert list(repeat('switch', 3)) not in [e['task transition'][i:i+3] for i in range(len(e['task transition']) - 3)]
        assert list(repeat('repeat', 3)) not in [e['response transition'][i:i+3] for i in range(len(e['response transition']) - 3)]
        assert list(repeat('switch', 3)) not in [e['response transition'][i:i+3] for i in range(len(e['response transition']) - 3)]

