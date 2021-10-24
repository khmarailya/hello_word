import math
import itertools
import random
import pytest

from src.Figure import Figure
from src.Triangle import Triangle
from src.Rectangle import Rectangle
from src.Square import Square
from src.Circle import Circle


def define_side_by_tmpl(check_side: str, sides, templates):
    for side, template in zip(sides, templates):
        if template == check_side:
            return side


def split_figure_args(str_args: str):
    return tuple(int(s.strip()) for s in str_args.strip().split(','))


SIMPLE_FIGURES_1 = [
    (Triangle, '3, 4, 5'),
    (Rectangle, '3, 4'),
    (Square, '3'),
    (Circle, '3'),
]

SIMPLE_FIGURES_2 = [
    (Triangle, '4, 5, 6'),
    (Rectangle, '4, 5'),
    (Square, '4' ),
    (Circle, '4'),
]

ERROR = .0001


@pytest.fixture
def make_fixture_figure(request):
    def wrapper(cls, *args, **kwargs):

        figure: Figure = cls(*args, **kwargs)
        request.addfinalizer(figure.__del__)
        return figure

    return wrapper


class TestRunFigure:

    @pytest.mark.xfail(raises=(ValueError,))
    def test_create_negative(self):
        """ фигура не д.б. создана"""
        Figure()

    @pytest.mark.parametrize('cls, str_args', [
        (Triangle, '0, 0, 0'),
        (Triangle, '-1, -1, -1'),
        (Rectangle, '0, 0'),
        (Rectangle, '-1, -1'),
        (Square, '0'),
        (Square, '-1'),
        (Circle, '0'),
        (Circle, '-1'),
    ])
    def test_create_negative_trivial(self, cls, str_args):
        """ фигура-наследник получает некорректные параметры - должна вернуть None"""
        assert cls(*split_figure_args(str_args)) is None

    @pytest.mark.parametrize('side1, msg', [
        (4, 'side1 > side2 + side3'),
        (3, 'side1 = side2 + side3')
    ])
    @pytest.mark.parametrize('side2 , side3', [
        (1, 2),
    ])
    @pytest.mark.parametrize('templates', (s[0] + s[1] + s[2] for s in itertools.permutations('abc')))
    def test_create_triangle_negative(self, side1, side2, side3, msg, templates):
        """ у треугольника особые требования к сторонам, получает некорректные - должен вернуть None
        также результат не должен зависеть от порядка следования сторон """
        sides = tuple(define_side_by_tmpl(t, (side1, side2, side3), templates) for t in templates)
        assert Triangle(*sides) is None


class TestRunName:

    @pytest.mark.parametrize('name', ['', 'q', 'Q', '1', ' '])
    @pytest.mark.parametrize('cls, str_args', SIMPLE_FIGURES_1)
    def test_name(self, name, cls, str_args, make_fixture_figure):
        """ простая фигура-наследник получает значение имени """
        assert make_fixture_figure(cls, *split_figure_args(str_args), name=name).name == name


class TestRunPerimeter:
    """ фигуры задаются сторонами, проверяется периметр
    допускается погрешность"""

    @pytest.mark.parametrize('a, b, c, res',
        [[*sides, 12] for sides in random.sample(tuple(itertools.permutations((3, 4, 5))), 3)]
        + [[*sides, 1.5 + math.sqrt(2)] for sides in random.sample(tuple(itertools.permutations((1, .5, math.sqrt(2)))), 3)]
    )
    def test_triangle_perimeter(self, a, b, c, res):
        """ результат не должен зависеть от порядка следования сторон
        прогон ограничен случайной выборкой из перебора порядка сторон
        (например, для многоугольника перебирать все нецелесообразно,
        подобная случайная выборка за несколько прогонов покроет все кейсы перестановок)"""
        assert abs(Triangle(a, b, c).perimeter - res) < ERROR

    @pytest.mark.parametrize('a, b, res',
        [[*sides, 14] for sides in tuple(itertools.permutations((3, 4)))]
        + [[*sides, 1 + math.sqrt(2)] for sides in tuple(itertools.permutations((.5, math.sqrt(2)/2)))]
    )
    def test_rectangle_perimeter(self, a, b, res):
        """ результат не должен зависеть от порядка следования сторон """
        assert abs(Rectangle(a, b).perimeter - res) < ERROR

    @pytest.mark.parametrize('a, res', [
        (1, 4),
        (math.sqrt(2)/4, math.sqrt(2)),
    ])
    def test_square_perimeter(self, a, res):
        assert abs(Square(a).perimeter - res) < ERROR

    @pytest.mark.parametrize('r, res', [
        (1, 2*math.pi),
        (math.pi, 2*(math.pi ** 2)),
    ])
    def test_circle_perimeter(self, r, res):
        assert abs(Circle(r).perimeter - res) < ERROR


class TestRunArea:
    """ фигуры задаются сторонами, проверяется площадь
    допускается погрешность"""

    @pytest.mark.parametrize('a, b, c, res',
        [[*sides, 6] for sides in random.sample(tuple(itertools.permutations((3, 4, 5))), 3)]
        + [[*sides, .5] for sides in random.sample(tuple(itertools.permutations((1, 1, math.sqrt(2)))), 3)]
    )
    def test_triangle_area(self, a, b, c, res):
        """ результат не должен зависеть от порядка следования сторон
        прогон ограничен случайной выборкой из перебора порядка сторон
        (например, для многоугольника перебирать все нецелесообразно,
        подобная случайная выборка за несколько прогонов покроет все кейсы перестановок)"""
        assert abs(Triangle(a, b, c).area - res) < ERROR

    @pytest.mark.parametrize('a, b, res',
        [[*sides, 12] for sides in tuple(itertools.permutations((3, 4)))]
        + [[*sides, 1] for sides in tuple(itertools.permutations((1/math.sqrt(2), math.sqrt(2))))]
    )
    def test_rectangle_area(self, a, b, res):
        """ результат не должен зависеть от порядка следования сторон """
        assert abs(Rectangle(a, b).area - res) < ERROR

    @pytest.mark.parametrize('a, res', [
        (1, 1),
        (math.sqrt(2), 2),
    ])
    def test_square_area(self, a, res):
        assert abs(Square(a).area - res) < ERROR

    @pytest.mark.parametrize('r, res', [
        (1, math.pi),
        (math.pi, math.pi ** 3),
    ])
    def test_circle_area(self, r, res):
        assert abs(Circle(r).area - res) < ERROR


class TestRunAddArea:

    @pytest.mark.parametrize('cls1, str_args1', SIMPLE_FIGURES_1)
    @pytest.mark.parametrize('cls2, str_args2', SIMPLE_FIGURES_2)
    @pytest.mark.parametrize('order', ['->', '<-',
    ])
    def test_add_area(self, cls1, str_args1, cls2, str_args2, order):
        """ проверив в других тестах, что площадь считается корректно,
        можно полагать, что сумма корректных площадей равна результату метода
        не должно зависеть от порядка аргументов """
        figure1, figure2 = cls1(*split_figure_args(str_args1)), cls2(*split_figure_args(str_args2))
        if order == '<-':
            figure1, figure2 = figure2, figure1
        assert figure1.area + figure2.area == figure1.add_area(figure2)











