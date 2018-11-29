import operator as op
import pytest

from sweetpea.primitives import Factor, DerivedLevel, WithinTrial

color = Factor("color", ["red", "blue"])
text = Factor("text", ["red", "blue"])

con_level  = DerivedLevel("con", WithinTrial(op.eq, [color, text]))
inc_level  = DerivedLevel("inc", WithinTrial(op.ne, [color, text]))
con_factor = Factor("congruent?", [con_level, inc_level])


def test_factor_validation():
    Factor("factor name", ["level 1", "level 2"])

    # Non-string name
    with pytest.raises(ValueError):
        Factor(56, ["level "])

    # Non-list levels
    with pytest.raises(ValueError):
        Factor("name", 42)

    # Empty list
    with pytest.raises(ValueError):
        Factor("name", [])


def test_factor_is_derived():
    assert color.is_derived() == False
    assert con_factor.is_derived() == True


def test_derived_level_get_dependent_cross_product():
    assert con_level.get_dependent_cross_product() == [
        (('color', 'red'), ('text', 'red')),
        (('color', 'red'), ('text', 'blue')),
        (('color', 'blue'), ('text', 'red')),
        (('color', 'blue'), ('text', 'blue'))]

    integer = Factor("integer", ["1", "2"])
    numeral = Factor("numeral", ["I", "II"])
    text = Factor("text", ["one", "two"])
    two_con_level = DerivedLevel("twoCon", WithinTrial(lambda x: x, [integer, numeral, text]))
    assert two_con_level.get_dependent_cross_product() == [
        (('integer', '1'), ('numeral', 'I'), ('text', 'one')),
        (('integer', '1'), ('numeral', 'I'), ('text', 'two')),
        (('integer', '1'), ('numeral', 'II'), ('text', 'one')),
        (('integer', '1'), ('numeral', 'II'), ('text', 'two')),
        (('integer', '2'), ('numeral', 'I'), ('text', 'one')),
        (('integer', '2'), ('numeral', 'I'), ('text', 'two')),
        (('integer', '2'), ('numeral', 'II'), ('text', 'one')),
        (('integer', '2'), ('numeral', 'II'), ('text', 'two'))]