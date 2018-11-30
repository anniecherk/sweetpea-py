import operator as op

from sweetpea.internal import get_all_level_names
from sweetpea.primitives import Factor, DerivedLevel, Transition


color = Factor("color", ["red", "blue"])
text  = Factor("text",  ["red", "blue", "green"])

color_repeats_level   = DerivedLevel("yes", Transition(op.eq, [color, color]))
color_no_repeat_level = DerivedLevel("no", Transition(op.ne, [color, color]))
color_repeats_factor  = Factor("color repeats?", [color_repeats_level, color_no_repeat_level])

def test_get_all_level_names():
    assert get_all_level_names([color, text]) == [('color', 'red'),
                                                  ('color', 'blue'),
                                                  ('text', 'red'),
                                                  ('text', 'blue'),
                                                  ('text', 'green')]

    assert get_all_level_names([color_repeats_factor]) == [('color repeats?', 'yes'),
                                                           ('color repeats?', 'no')]