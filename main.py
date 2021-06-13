class TypesValidator:
    def __init__(self, func):
        self.func: function = func
        self.annotations: dict = self.func.__annotations__

    def __call__(self, *args, **kwargs):

        error_messages = list()
        error_messages.extend(self._args_parser(args))
        error_messages.extend(self._kwargs_parser(kwargs))

        if error_messages:
            message = f"Function got {len(error_messages)} wrong inputs:\n" + "\n".join(error_messages)
            raise TypeError(message)

        result = self.func(*args, **kwargs)

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


