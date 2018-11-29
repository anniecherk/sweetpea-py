from typing import List, Tuple, Union, Any
from functools import reduce
from itertools import product

from sweetpea.primitives import WithinTrial, Transition, Window
from sweetpea.blocks import Block
from sweetpea.constraints import Derivation
from sweetpea.internal import get_all_level_names


class DerivationProcessor:
    """
    Useage::
        >>> import operator as op
        >>> color = Factor("color", ["red", "blue"])
        >>> text  = Factor("text",  ["red", "blue"])
        >>> conLevel  = DerivedLevel("con", WithinTrial(op.eq, [color, text]))
        >>> incLevel  = DerivedLevel("inc", WithinTrial(op.ne, [color, text]))
        >>> conFactor = Factor("congruent?", [conLevel, incLevel])
        >>> design = [color, text, conFactor]
        >>> crossing = [color, text]
        >>> __process_derivations(design, crossing)
        [Derivation(derivedIdx=4, dependentIdxs=[[0, 2], [1, 3]]), Derivation(derivedIdx=5, dependentIdxs=[[0, 3], [1, 2]])]
    rtype: returns a list of tuples. Each tuple is structured as:
            (index of the derived level, list of dependent levels)
    In the example above, the indicies of the design are:
        idx: level:
        0    color:red
        1    color:blue
        2    text:red
        3    text:blue
        4    conFactor:con
        5    conFactor:inc
    So the tuple (4, [[0,2], [1,3]]) represents the information that
        the derivedLevel con is true iff
            (color:red && text:red) ||
            (color:blue && text:blue)
        by pairing the relevant indicies together.
    """
    @staticmethod
    def generate_derivations(block: Block) -> List[Derivation]:
        design = block.design
        derived_factors = list(filter(lambda f: f.is_derived(), block.design))
        all_levels = get_all_level_names(design)
        accum = []
        for fact in derived_factors:
            for level in fact.levels:
                level_index = all_levels.index((fact.name, level.name))

                # Shift level index for complex windows
                if fact.has_complex_window():
                    difference = level_index - block.variables_per_trial()
                    level_index = difference + block.grid_variables()

                x_product = level.get_dependent_cross_product()
                # filter to valid tuples, and get their idxs
                valid_tuples = [tup for tup in x_product if level.window.fn(*map(lambda t: t[1], tup))]
                valid_idxs = [[all_levels.index(level) for level in tup] for tup in valid_tuples]
                shifted_idxs = DerivationProcessor.shift_window(valid_idxs, level.window, block.variables_per_trial())
                accum.append(Derivation(level_index, shifted_idxs))
        return accum

    """
    This is a helper function that shifts the idxs of __process_derivations.
    ie, if its a Transition(op.eq, [color, color]) (ie "repeat" color transition)
        then the indexes for the levels of color would be like (0, 0), (1, 1)
        but actually, the window size for a transition is 2, so what we really want is the indicies
        (0, 5), (1, 6) (assuming there are 4 levels in the design)
    So this helper function shifts over indices that were meant to be intepretted as being in a subsequent trial.
    """
    @staticmethod
    def shift_window(idxs: List[List[int]],
                     window: Union[WithinTrial, Transition, Window],
                     trial_size:int) -> List[List[int]]:
        if isinstance(window, WithinTrial):
            return idxs
        elif isinstance(window, Transition):
            return [[pair[0], pair[1]+trial_size] for pair in idxs]
        elif isinstance(window, Window):
            return [reduce(lambda l, idx: l + [idx + len(l) * trial_size], idx_list, []) for idx_list in idxs]
        else:
            raise ValueError("Weird window encountered while processing derivations!")