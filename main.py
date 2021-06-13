from typing import Callable

class TypesValidator:
    def __init__(self, func: Callable, check_return: bool=False):
        self.func = func
        self.annotations = self.func.__annotations__
        self.check_return = check_return

    def __call__(self, *args, **kwargs):

        error_messages = list()
        error_messages.extend(self._args_parser(args))
        error_messages.extend(self._kwargs_parser(kwargs))

        if error_messages and not self.check_return:
            message = f"Function got {len(error_messages)} wrong inputs:\n" + "\n".join(error_messages)
            raise TypeError(message)

        result = self.func(*args, **kwargs)

        if self.check_return:
            if not isinstance(result, self.annotations['return']):
                error_messages.append(f"Type of return is not correct. Should be {self.annotations['return']}, but got {result.__class__}")

        if error_messages:
            message = f"Function got {len(error_messages)} wrong inputs:\n" + "\n".join(error_messages)
            raise TypeError(message)

        return result

    def _args_parser(self, args):
        errors = list()

        for arg, key in zip(args, self.annotations.keys()):
            is_correct = isinstance(arg, self.annotations[key])
            if not is_correct:
                errors.append(
                    f'Argument "{key}" type is not correct: should be {self.annotations[key]}, but got {arg.__class__}'
                )

        return errors

    def _kwargs_parser(self, kwargs):
        errors = list()

        for kwarg in kwargs:
            is_correct = isinstance(kwargs[kwarg], self.annotations[kwarg])
            if not is_correct:
                errors.append(
                    f'Argument "{kwarg}" type is not correct: should be {self.annotations[kwarg]}, but got {kwargs[kwarg].__class__}'
                )

        return errors

def validate_types(check_return: bool=False):
    def _check(function):
        return TypesValidator(function, check_return)
    return _check


