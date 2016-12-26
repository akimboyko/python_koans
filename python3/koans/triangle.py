#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.

# Triangle analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#

import itertools


def triangle(a, b, c):
    if any(s <= 0 for s in [a, b, c]):
        raise TriangleError()
    elif any(s1 > s2 + s3 for s1, s2, s3 in itertools.permutations([a, b, c])):
        raise TriangleError()
    elif a == b == c:
        return 'equilateral'
    elif a == b or b == c or a == c:
        return 'isosceles'
    else:
        return 'scalene'

# Error class used in part 2.  No need to change this code.
class TriangleError(Exception):
    pass
