from src.Figure import Figure


class Square(Figure):

    def __init__(self, a: float, name: str = None):
        super().__init__(name)
        self.a = a

    @classmethod
    def check_correct(cls, a: float, name: str = None) -> bool:
        return cls.check_side(a)

    @property
    def area(self) -> float:
        return self.a * self.a

    @property
    def perimeter(self) -> float:
        return 4 * self.a


if __name__ == '__main__':
    pass




