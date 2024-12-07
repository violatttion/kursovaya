import unittest
from figure import circle_area, circle_perimeter
from figure import square_area, square_perimeter
from figure import triangle_area, triangle_perimeter


class TestFigure(unittest.TestCase):

    def test_circle(self):
        self.assertAlmostEqual(circle_area(5), 78.53981633974483)
        self.assertAlmostEqual(circle_perimeter(5), 31.41592653589793)

    def test_square(self):
        self.assertEqual(square_area(3), 9)
        self.assertEqual(square_perimeter(3), 12)
        # значение по умолчанию
        self.assertEqual(square_area(), 225)
        self.assertEqual(square_perimeter(), 60)

    def test_triangle(self):
        # Ожидаем значение, рассчитанное с использованием формулы Герона
        self.assertAlmostEqual(triangle_area(7, 2, 8),6.437196594791867)
        self.assertEqual(triangle_perimeter(7, 2, 8), 17)
        # Проверяем значения по умолчанию, если они есть
        self.assertAlmostEqual(triangle_area(5, 5, 5), 10.825317547305486)
        self.assertEqual(triangle_perimeter(5, 5, 5), 15)


if __name__ == '__main__':
    unittest.main()