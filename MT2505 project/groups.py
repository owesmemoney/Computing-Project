# -*- coding: utf-8 -*-
"""
Created on Wed Feb 4 2015
Modified for python 3 Monday Mar 11 2019

order command created by MRQ 23.ii.20

@author: James D. Mitchell
"""

###############################################################################

from itertools import combinations
from math import factorial

###############################################################################
# Perms
###############################################################################


class Perm:
    # private data for degree and largest moved point
    _deg = None
    _lmp = None

    def __init__(self, *args):
        if len(args) == 0:
            self._deg = 0
            self.image = []
        elif type(args[0]) is tuple:
            # Check args and find degree
            deg = 0
            for tup in args:
                if not type(tup) is tuple:
                    raise ValueError
                if len(tup) > 0 and max(tup) > deg:
                    deg = max(tup)
            # check injective
            seen = [False] * deg

            for tup in args:
                for i in tup:
                    if seen[i - 1]:
                        raise ValueError
                    else:
                        seen[i - 1] = True
            # install the values
            self.image = list(range(deg))
            for tup in args:
                for i in range(len(tup)):
                    self.image[tup[i] - 1] = tup[(i + 1) % len(tup)] - 1
            self._deg = deg
        elif type(args[0]) is int:
            # permutation defined by list of images
            self.image = list(args)
        else:
            raise ValueError

    def __pow__(self, i):
        '''power a Perm by an integer '''
        if not type(i) is int:
            raise TypeError
        if i == 0:
            return Perm()
        if i > 0:
            perm = self.copy()
            j = 0
            while j < i - 1:
                j += 1
                perm = perm * self
            return perm
        elif i < 0:
            return self.inverse() ** -i

    def __eq__(self, right):
        '''check equality of Perms'''
        deg = max(self.degree(), right.degree())
        for i in range(deg):
            if self[i] != right[i]:
                return False
        return True

    def __ne__(self, right):
        '''check inequality of Perms'''
        deg = max(self.degree(), right.degree())
        deg = max(self.degree(), right.degree())
        for i in range(deg):
            if self[i] != right[i]:
                return True
        return False

    def __getitem__(self, index):
        '''find the image of <index> under <self>, INTERNAL ONLY.
           returns self.image[index] which is shifted by 1!
        '''
        if index < self.degree():
            return self.image[index]
        else:
            return index

    def __repr__(self):
        ''' print out as a product of disjoint cycles'''
        out = ''
        seen = [False] * self.degree()
        for i in range(self.degree()):
            if not seen[self[i]]:
                seen[i] = True
                j = self[i]
                if j != i:
                    out += '(' + str(i + 1)
                    while self[j] != i:
                        seen[j] = True
                        out += ' ' + str(j + 1)
                        j = self[j]
                    seen[j] = True
                    out += ' ' + str(j+1) + ')'
        if out == '':
            out = '()'
        return out

    def __mul__(self, right):
        deg = max(self.degree(), right.degree())
        image = list(range(deg))
        for i in range(deg):
            image[i] = self[right[i]]

        return Perm(*image)

    def __hash__(self):
        return hash(tuple(self.image[0:self.lmp()]))

    def identity(self):
        return Perm(*list(range(self.degree())))

    def copy(self):
        '''copy a Perm, INTERNAL ONLY'''
        return Perm(*self.image)

    def inverse(self):
        '''invert a Perm, INTERNAL ONLY, use ** -1 externally'''
        image = list(range(self.degree()))
        for i in range(self.degree()):
            image[self[i]] = i
        return Perm(*image)

    def lmp(self):
        '''
        Find the largest moved point of the perm, INTERNAL ONLY.

        Corrected 17/04/2018 as pointed out by Reinis Cirpons in MT2505, the
        previous version did not return the largest moved point, and but the
        smallest moved point, and this caused equal perms to have different
        hash values.
        '''
        if self._lmp is None:
            self._lmp = 0
            for i in range(self.degree(), 0, -1):
                if self[i] != i:
                    self._lmp = i
                    break

        return self._lmp

    def degree(self):
        '''find the degree of a perm, i.e. the largest value in the list of
        images. This is not necessarily the same as the largest moved point
        (i.e. it can be larger)
        '''
        if self._deg is None:
            deg = 0
            for i in self.image:
                if i + 1 > deg:
                    deg = i + 1
            self._deg = deg
        return self._deg

    def hit(self, i):
        if isinstance(i, int):
            if i >= 0:
                return self[i - 1] + 1
            else:
                raise ValueError
        else:
            raise TypeError

###############################################################################
# Symmetric groups
###############################################################################


class SymmetricGroup:
    _nr_next_emitted = 0
    _size = None

    def __init__(self, deg):
        self._deg = deg
        self._current = list(range(self.degree() - 1, 0, -1))
        self._transpositions = []
        i = 0
        while i < self.degree():
            self._transpositions.append([None] * self.degree())
            i += 1

    def identity(self):
        '''return the identity of the group'''
        return Perm()

    def __repr__(self):
        return "<symmetric group on " + str(self.degree()) + " points>"

    def __contains__(self, perm):
        if isinstance(perm, Perm):
            return perm.degree() <= self.degree()

    def degree(self):
        '''returns the number of points acted on'''
        return self._deg

    def size(self):
        '''returns the size of the group'''
        if self._size is None:
            self._size = factorial(self.degree())
        return self._size

    def order(self):
        """Returns the order of the group"""
        # This just calls the size command, but MRQ prefers the term
        # 'order' for a group.
        return self.size()

    def transpose(self, i, j):
        '''This is a cache for transpositions to speed things up.
           Returns the transposition (i, j) when i < j'''
        if i > j:
            i, j = j, i
        if not isinstance(self._transpositions[i][j], Perm):
            if i != j:
                self._transpositions[i][j] = Perm((i + 1, j + 1))
            else:
                self._transpositions[i][j] = Perm()
        return self._transpositions[i][j]

    def __iter__(self):
        self._current = list(range(self.degree() - 1, 0, -1))
        return self

    def __next__(self):
        '''
        Returns the next element of the group. Uses basic stabiliser chain,
        and transpositions.
        '''
        if self._nr_next_emitted == self.size():
            self._nr_next_emitted = 0
            raise StopIteration
        self._nr_next_emitted += 1
        pos = self.degree() - 1
        perm = Perm()
        while pos > 0:
            pos -= 1
            self._current[pos] = ((self._current[pos] + 1)
                                  % (self.degree() - pos))
            perm *= self.transpose(pos, self._current[pos] + pos)
            if self._current[pos] != 0:
                break
        while pos > 0:
            pos -= 1
            perm *= self.transpose(pos, self._current[pos] + pos)
        return perm

###############################################################################
# IsSymmetricGroup
###############################################################################


def IsSymmetricGroup(obj):
    '''check the object is a group (within the narrow definition of the things
       implemented in this file).
    '''
    return isinstance(obj, SymmetricGroup)


def IsPerm(obj):
    '''check the object is a group (within the narrow definition of the things
       implemented in this file).
    '''
    return isinstance(obj, Perm)
