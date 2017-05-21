from vector import Vector
from line import Line

l1 = Line(Vector([4.046, 2.836]), 1.21)
l2 = Line(Vector([10.115, 7.09]), 3.025)
print l1.intersection_with(l2)

l1 = Line(Vector([7.204, 3.182]), 8.68)
l2 = Line(Vector([8.172, 4.114]), 9.883)
print l1.intersection_with(l2)

l1 = Line(Vector([1.182, 5.562]), 6.744)
l2 = Line(Vector([1.773, 8.343]), 9.525)
print l1.intersection_with(l2)
