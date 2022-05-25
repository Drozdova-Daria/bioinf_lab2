class Function:
    def __init__(self, func: str) -> None:
        self.function = (lambda x1=0, x2=0: eval(func))
        self.func_str = func
        self.args_count = 2

    def __str__(self) -> str:
        return self.func_str

    def __call__(self, *args):
        return self.function(*args)

