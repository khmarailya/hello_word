class Figure:

    COUNT = 0

    def __init__(self, name: str = None):
        if self.__class__ == Figure:
            raise ValueError('Создавать экземпляры базового класса Figure запрещено')

        self.__class__.COUNT += 1
        self.name = name
        self._index = self.__class__.COUNT

    def __new__(cls, *args, **kwargs):
        if not cls.check_correct(*args, **kwargs):
            return None

        return super(Figure, cls).__new__(cls)

    def raise_incorrect(self):
        raise ValueError(f'{self} - фигура задана некорректно')

    def __del__(self):
        del self

    @property
    def area(self) -> float:
        raise NotImplementedError('Необходимо реализовать вычисление площади')

    @property
    def perimeter(self) -> float:
        raise NotImplementedError('Необходимо реализовать вычисление периметра')

    def add_area(self, figure: 'Figure') -> float:
        if not isinstance(figure, Figure):
            raise ValueError(f'Передан неправильный класс ({figure})')
        return self.area + figure.area

    @staticmethod
    def check_side(a: float) -> bool:
        return a > 0

    @classmethod
    def check_correct(cls, *args, **kwargs) -> bool:
        return True

    def __str__(self):
        return f'{self.name} ({self.__class__.__name__}{self._index})'
