from typing import Any, Type, List, Tuple
from itertools import product


class __Primitive:
    def require_type(self, label: str, type: Type, value: Any):
        if not isinstance(value, type):
            raise ValueError(label + ' must be a ' + str(type) + '.')


    def require_non_empty_list(self, label: str, value: Any):
        self.require_type(label, List, value)
        if len(value) == 0:
            raise ValueError(label + ' must not be empty.')


class Factor(__Primitive):
    def __init__(self, name: str, levels) -> None:
        self.name = name
        self.levels = levels
        self.__validate()

    def __validate(self):
        self.require_type('Factor.name', str, self.name)
        self.require_non_empty_list('Factor.levels', self.levels)
        level_type = type(self.levels[0])
        if level_type not in [str, DerivedLevel]:
            raise ValueError('Factor.levels must be either string or DerivedLevel')
    
        for l in self.levels:
            if type(l) != level_type:
                raise ValueError('Expected all levels to be ' + str(level_type) + 
                    ', but found ' + str(type(l)) + '.')

        if level_type == DerivedLevel:
            window_type = type(self.levels[0].window)
            for dl in self.levels:
                if type(dl.window) != window_type:
                    raise ValueError('Expected all DerivedLevel.window types to be ' + 
                        str(window_type) + ', but found ' + str(type(dl)) + '.')

    def is_derived(self) -> bool:
        return isinstance(self.levels[0], DerivedLevel)

    def has_complex_window(self) -> bool:
        return self.is_derived() and not isinstance(self.levels[0].window, WithinTrial)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class DerivedLevel(__Primitive):
    def __init__(self, name, window):
        self.name = name
        self.window = window
        self.__validate()

    def __validate(self):
        self.require_type('DerivedLevel.name', str, self.name)
        window_type = type(self.window)
        allowed_window_types = [WithinTrial, Transition, Window]
        if window_type not in allowed_window_types:
            raise ValueError('DerivedLevel.window must be one of ' + 
                str(allowed_window_types) + ', but was ' + str(window_type) + '.')
        # TODO: Windows should be uniform.

    def get_dependent_cross_product(self) -> List[Tuple[Any, ...]]:
        return list(product(*[[(dependent_factor.name, x) for x in dependent_factor.levels] for dependent_factor in self.window.args]))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class __BaseWindow():
    def __init__(self, fn, args, width: int, stride: int) -> None:
        self.fn = fn
        self.args = args
        self.width = width
        self.stride = stride
        # TODO: validation


class WithinTrial(__Primitive, __BaseWindow):
    def __init__(self, fn, args):
        super().__init__(fn, args, 1, 1)
        # TODO: validation

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Transition(__Primitive, __BaseWindow):
    def __init__(self, fn, args):
        super().__init__(fn, args, 2, 1)
        # TODO: validation

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Window(__Primitive, __BaseWindow):
    def __init__(self, fn, args, stride):
        super().__init__(fn, args, len(args), stride)
        # TODO: validation

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)