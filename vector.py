import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    MSG_NORM_ZERO_VECTOR = 'Cannot normalize the zero vector'
    MSG_ANGL_ZERO_VECTOR = 'Cannot compute angle with the zero vector'
    MSG_DOT_DIF_DIM = 'Cannot perform dot products on vector with different dimensions'

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
        nc = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(nc)

    def minus(self, v):
        nc = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(nc)

    def times_scalar(self, c):
        nc = [c*x for x in self.coordinates]
        return Vector(nc)

    def magnitude(self):
        sq = [x*x for x in self.coordinates]
        return Decimal(math.sqrt(sum(sq)))

    def normalization(self):
        try:
            mag = self.magnitude()
            return self.times_scalar(Decimal(1)/mag)
        except ZeroDivisionError:
            raise Exception(self.MSG_NORM_ZERO_VECTOR)

    def dot(self, v):
        if (self.dimension != v.dimension):
            raise Exception(MSG_DOT_DIF_DIM)

        dot = Decimal(sum([x*y for x,y in zip(self.coordinates, v.coordinates)]))

        # NOT a nice workaround!!!!!
        if dot > 1:
            return Decimal(1)
        elif dot < -1:
            return Decimal(-1)
        else:
            return dot

    def angle_with(self, v, in_degrees=False):
        
        try:
            rad = math.acos(self.normalization().dot(v.normalization()))
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


v = Vector([-7.579, -7.88])
w = Vector([22.737, 23.64])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)

v = Vector([-2.029, 9.97, 4.172])
w = Vector([-9.231, -6.639, -7.245])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)

v = Vector([-2.328, -7.284, -1.214])
w = Vector([-1.821, 1.072, -2.94])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)

v = Vector([2.118, 4.827])
w = Vector([0, 0])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)

