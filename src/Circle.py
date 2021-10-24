from src.Figure import Figure
import math


class Circle(Figure):

    def __init__(self, r: float, name: str = None):
        super().__init__(name)
        self.r = r

    @classmethod
    def check_correct(cls, r: float, name: str = None) -> bool:
        return cls.check_side(r)

    @property
    def area(self) -> float:
        return math.pi * self.r * self.r

    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self.r


if __name__ == '__main__':
    pass




