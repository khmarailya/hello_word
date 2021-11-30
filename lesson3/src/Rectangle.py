from src.Figure import Figure


class Rectangle(Figure):

    def __init__(self, a: float, b: float, name: str = None):
        super().__init__(name)
        self.a = a
        self.b = b

    @classmethod
    def check_correct(cls, a: float, b: float, name: str = None) -> bool:
        return all([cls.check_side(side) for side in (a, b)])

    @property
    def area(self) -> float:
        return self.a * self.b

    @property
    def perimeter(self) -> float:
        return 2 * (self.a + self.b)


if __name__ == '__main__':
    pass




