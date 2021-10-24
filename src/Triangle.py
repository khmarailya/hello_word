from src.Figure import Figure

import math


class Triangle(Figure):

    def __init__(self, a: float, b: float, c: float, name: str = None):
        super().__init__(name=name)
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def check_correct(cls, a: float, b: float, c: float, name: str = None) -> bool:
        return not (a + b <= c or a + c <= b or c + b <= a)

    @property
    def area(self) -> float:
        """
            S = sqr(2)(p⋅(p−a)⋅(p−b)⋅(p−c))
            p = (a+b+c)/2
        """
        p = self.perimeter/2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    @property
    def perimeter(self) -> float:
        return self.a + self.b + self.c


if __name__ == '__main__':
    pass





