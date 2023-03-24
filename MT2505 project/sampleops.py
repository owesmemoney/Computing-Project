# Module:  sampleops
# Author:  Martyn Quick (based on some examples from JDM)
# Version: 0.5

__doc__ = """
Sample binary operations for use in first part of the MT2505 computing
project
"""

########################################
#
# HISTORY:
# 7.ii.20: Version 0.1 (File created)
# 8.ii.20: Version 0.2 (Fixed tripleop code to return integers in the list)
# 9.ii.20: Version 0.5 (File released to students after some bug-testing)
#
########################################


# Binary operations for use when debugging the
# is_associative_operation function
assoc_example = [
    [ [0]*7, [0]*7, [0]*7, [0]*7, [0,0,0,2,1,0,1], [0,0,0,2,1,1,2],
      [0,0,0,0,1,1,2] ],
    [ [0]*7, [0]*7, [0]*7, [0]*7, [0,0,0,2,1,0,1], [0,0,0,2,1,1,2],
      [0,0,0,0,1,1,6] ],
    [ [0]*7, [0,1,0,0,0,0,1], [0,0,2,2,2,2,0], [0,0,2,3,2,2,0],
      [0,0,2,2,4,4,0], [0,0,2,2,4,5,0], [0,1,0,0,0,0,6] ],
    [ [0,1,2,3,4], [1,0,4,2,3], [2,3,0,4,1], [3,4,1,0,2], [4,2,3,1,0]
    ],
    [ [0,1,2,3,4], [1,2,4,0,3], [2,4,3,1,0], [3,0,1,4,2], [4,3,0,2,1]
    ],
    [ [0]*5, [0]*5, [0]*5, [0]*5, [0,1,0,0,0] ] ]

# Binary operations for use when debugging the identity_of_operation
# function
id_example = [
    [ [0,1,2,3,4], [1,0,4,2,3], [2,3,0,4,1], [3,4,1,0,2], [4,2,3,1,0]
    ],
    [ [0,1,2,3,4], [1,2,4,0,3], [2,4,3,1,0], [3,0,1,4,2], [4,3,0,2,1]
    ],
    [ [0]*5, [0]*5, [0]*5, [0]*5, [0,1,0,0,0] ],
    [ [0,0,2,2,4,5,0], [0,0,2,2,4,5,1], [2,2,0,0,5,4,2],
      [2,2,0,0,5,4,3], [4,4,5,5,0,2,4], [5,5,4,4,2,0,5],
      [0,1,2,3,4,5,6] ],
    [ [0]*7, [0,0,1,1,0,1,1], [0,0,2,3,0,2,6], [0,0,3,2,0,3,6], [4]*7,
      [0,1,2,3,4,5,6], [0,0,6,6,0,6,6] ],
    [ [0,1,2,3,4,4,3], [1,2,4,0,3,3,0], [2,4,3,1,0,0,1],
      [3,0,1,4,2,2,4], [4,3,0,2,1,1,2], [4,3,0,2,1,1,2],
      [3,0,1,4,2,2,5] ] ]


# Command to convert an integer to its representation in base 3 (as a
# string).  This is used in the tripleop function.
def _BaseThree(n):
    if n < 3:
        return "%d" % n
    else:
        return (_BaseThree(n//3) + "%d" % (n%3))


# Command to generate one of the 3^9 binary operations on the set
# [0,1,2].  The input variable must be in the range  0 <= n <=
# (3^9)-1.
def tripleop(n):
    if n in range(3**9):
        x = _BaseThree(n)
        l = len(x)
        x = ("0"*9)[:-l] + x
        return [ [ int(x[0]), int(x[1]), int(x[2]) ],
                 [ int(x[3]), int(x[4]), int(x[5]) ],
                 [ int(x[6]), int(x[7]), int(x[8]) ] ]
    else:
        print("Input variable not in correct range")
        return False
