#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID: 190026112
MT2505:  Computing Project
"""
import random 
from sampleops import tripleop



#Question 1
# to check the property of binary operation by checking if the 
# element contained in the list is list and if the number inside 
# the element is less than the length of the list based on the 
# property of the cayley table
def is_binary_operation (X):
    if not isinstance (X, list ):
        return False
    for entry in X:
        if not isinstance(entry, list):
            return False
        if len(entry)!=len(X):
            return False
        for value in entry:
            if not isinstance(value, int):
                return False
            if not value < len(entry):
                return False
    return True



# Question 2
# the function to create random binary operation 
# on the set {0, 1, ..., n-1} for any positive integer n
def random_binary_operation (n):
    out = []
    for i in range (n):
        out. append ([])
        for j in range (n):
            out[i].append([])
            out[i][j]=random.randint(0,n-1)
    return out

 
    
#Question 3
# determine whether a binary operationon is associative or not
# by accessing elemnts in matrix X
# in the function a represnts the x*y, so b represents (x*y)*z
# similarly, c represents y*z, and d represents x*(y*z)
# and then check if b=d which is associative
def is_associative_operation (X):
    if not is_binary_operation (X):
        return False
    n=len(X)
    for i in range(0,n):
        for j in range(0,n):
            for e in range(0,n):
                a=X[i][j]
                b=X[a][e]
                c=X[j][e]
                d=X[i][c]
                if b!=d:
                    return False
    return True         




# Question 4
# takes a binary operation (a list of lists) as an argument 
# and returns e that is an identity for the operation if it exists
# and returns -1 if there is no identity element
def identity_of_operation(X):
    n=len(X)
    result=[]
    for i in range(n):
        result.append(i)
    for j in range(n):
        cur_row = X[j]
        cur_col=[row[j] for row in X]
        # the property of identity shown in cayley table
        # is that the row or column which the identity belongs to
        # are the same as the original element in list
        if cur_row ==result== cur_col:
            return j
    return -1
        



#Question 5
# the function to determine if the operation is commutative or not
def is_commutative_operation(X):
    if not is_binary_operation (X):
        return False
    n=len(X)
    for i in range(n):
        for j in range(n):
            if X[i][j]!=X[j][i]:
                return False
    return True

# the function to determine if every element in X has the inverse
def inverse_element(X):
    identity = identity_of_operation(X)
    if identity == -1:
        return False
    if not is_binary_operation (X):
        return False  
    for i in range(len(X)):
        found=False
        for j in range(len(X)):
            if X[i][j]==X[j][i]==identity:
                found= True
                break
        if not found:
            return False
    return True
            
                
                
    


# 5(a)            
a=sum (1 for n in range (3**9) if
is_associative_operation ( tripleop (n))==True and is_commutative_operation(tripleop(n))==False )
# returns 50, so there are 50 binary operations associative but not commutative


# 5(b)
b=sum (1 for n in range (3**9) if
is_associative_operation ( tripleop (n))==False and is_commutative_operation(tripleop(n))==True)
# returns 666, so there are 666 binary operations commutative but not associative

# 5(c)
c= sum (1 for n in range (3**9) if
is_associative_operation ( tripleop (n))==True and identity_of_operation(tripleop(n))!=-1 and inverse_element(tripleop(n))==True)
# returns 3, so there are 3 binary operations with the structure of a
#group


# 5(d)
d= sum (1 for n in range (3**9) if
is_associative_operation ( tripleop (n))==True and identity_of_operation(tripleop(n))!=-1 and inverse_element(tripleop(n))==True and is_commutative_operation(tripleop(n))==True)
# returns 3, so there are 3 binary operations with the structure of an abelian group



#Question 6
# the function to form the permutation
# eg. permutation in (a) turns to 
#[[1,2,3,4,5,6,7,8,9,10,11,12],[2,3,1,5,6,4,7,8,9,11,12,10]]
def form_permutation(x):
    rows,cols=(2,x.degree())
    perm = [[0 for i in range(cols)] for i in range(rows)]
    for i in range(x.degree()):
        perm[0][i] = i+1
        perm[1][i] = x.hit(i+1)
    return perm

# the function to change the permutation into the disjoint cycle in  list
# eg. permutation (a) turns to [[1,2,3],[4,5,6],[10,11,12]]
def from_permutation_to_disjoints_cycles(x):
    perm = form_permutation(x)
    mappings ={a:b for a,b in zip(*perm)}
    cycles = []
    for a in perm[0]:
        b =mappings.pop(a,None)
        if b is None:
            continue
        cycle = [a]
        while a !=b:
            cycle.append(b)
            b =mappings.pop(b)
        if len(cycle)>1:
            cycles.append(cycle)
    return cycles
 

# the function to find the length of the cycle where k lies
# just locate where the k is in the matrix and then 
# return the length of the length of the row where k lies
def cycle_length(x,k):
    length = 0
    cycle_list = from_permutation_to_disjoints_cycles(x)
    for i in range(len(cycle_list)):
        for j in range(len(cycle_list[i])):
            if cycle_list[i][j] ==k:
                length = len(cycle_list[i])
    return length
    
     

#Question 7
from math import gcd
from functools import reduce 

# the function to get the least common multiple of two variables
def lcm(a, b):
    return a * b // gcd(a, b)

# the function to get the least common multiple for a list
def get_lcm_for(your_list):
    return reduce(lambda x, y: lcm(x, y), your_list)

# the function to get the order of permutation by get the least common 
# multiple for all the disjoints cycles lengths
def order_perm(x):
    list=[]
    cycle_list = from_permutation_to_disjoints_cycles(x)
    lenl=len(cycle_list)
    for i in range(lenl):
        list.append(len(cycle_list[i]))
        ans=get_lcm_for(list)
    return ans  


#Question 8
import gzip,pickle,requests
from groups import*
open("vlp.p.gz", "wb").write(requests.get("https://tinyurl.com/bigperm2020").content)
p=pickle.load(gzip.open("vlp.p.gz", "r"))
# use order_perm function in Question 7
order_perm(p)
# Returns 29975171216047372011101965560

                
            
     