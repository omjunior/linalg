import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    MSG_NORM_ZERO_VECTOR = 'Cannot normalize the zero vector'
    MSG_ANGL_ZERO_VECTOR = 'Cannot compute angle with the zero vector'
    MSG_DIF_DIM = 'Operands need to have the same dimensions'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        if (self.dimension != v.dimension):
            raise Exception(MSG_DIF_DIM)

        nc = [Decimal(x+y) for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(nc)

    def minus(self, v):
        if (self.dimension != v.dimension):
            raise Exception(MSG_DIF_DIM)

        nc = [Decimal(x-y) for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(nc)

    def times_scalar(self, c):
        nc = [Decimal(c*x) for x in self.coordinates]
        return Vector(nc)

    def magnitude(self):
        sq = [Decimal(x*x) for x in self.coordinates]
        return Decimal(math.sqrt(sum(sq)))

    def normalized(self):
        try:
            mag = self.magnitude()
            return self.times_scalar(Decimal(1)/mag)
        except ZeroDivisionError:
            raise Exception(self.MSG_NORM_ZERO_VECTOR)

    def dot(self, v):
        if (self.dimension != v.dimension):
            raise Exception(MSG_DIF_DIM)

        return Decimal(sum([x*y for x,y in zip(self.coordinates, v.coordinates)]))

    def angle_with(self, v, in_degrees=False):
        if (self.dimension != v.dimension):
            raise Exception(MSG_DIF_DIM)

        try:
            cosang = self.normalized().dot(v.normalized())
            # precision workaround
            if cosang > 1:
                cosang = 1
            elif cosang < 0:
                cosang = 0

            rad = math.acos(cosang)
        except Exception as e:
            if str(e) == self.MSG_NORM_ZERO_VECTOR:
                raise Exception(self.MSG_ANGL_ZERO_VECTOR)
            else:
                raise e

        if (not in_degrees):
            return rad
        else:
            return math.degrees(rad)

    def is_orthogonal_to(self, v, epsilon=1e-10):
        return abs(self.dot(v)) < epsilon

    def is_parallel_to(self, v, epsilon=1e-10):
        if self.is_zero() or v.is_zero():
            return True
        angle = self.angle_with(v);
        if abs(angle) < epsilon:
            return True
        if abs(angle - math.pi) < epsilon:
            return True
        return False

    def is_zero(self, epsilon=1e-10):
        return (abs(self.magnitude()) < epsilon)

    def component_parallel_to(self, b):
        ub = b.normalized()
        return ub.times_scalar(self.dot(ub))

    def component_orthogonal_to(self, b):
        return self.minus(self.component_parallel_to(b))



v = Vector([3.039, 1.879])
b = Vector([0.825, 2.036])
print v.component_parallel_to(b)

v = Vector([-9.88, -3.264, -8.159])
b = Vector([-2.155, -9.353, -9.473])
print v.component_orthogonal_to(b)

v = Vector([3.009, -6.172, 3.692, -2.51])
b = Vector([6.404, -9.144, 2.759, 8.718])
print v.component_parallel_to(b)
print v.component_orthogonal_to(b)
