#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is a 3D python model of a Rubiks cube.
In this model, the cube's 6 pieces in the middle of the faces remain fixed.
All transformations take place by rotating one of the 6 faces, or by
rotating 2 opposite faces the same direction and angle.
So the X,Y,Z axes remain fixed to the pieces on the middle face.

The large 3x3 cube can be broken into 20 moving pieces.
Each piece is described as 6 integers:
    a 3-element vector to describe the piece's position
    a 3-element vector to describe the piece's rotation

There are 9 possible transformations at the piece level:
    rotate around X,Y, or Z axis; rotate 1,2, or 3 quarters.
Each transformation can be applied in 1 of 3 ways:
    to the face at the -axis, to the face at the +axis,
    or to the middle ring around that axis. Transformations
    around the middle ring are implemented as opposite rotations
    to the + and - faces.
That makes 27 total transformations, with the restriction that
    no 2 sequential transformations take place around the same axis.
    So calculating another move multiplies the calculations needed by 18.
"""

import numpy
import itertools
from random import randint

#Build transformation matrices
#straightforward linear algebra
X1q=numpy.array([[1,0,0,0,0,0],[0,0,-1,0,0,0],[0,1,0,0,0,0],
                 [0,0,0,1,0,0],[0,0,0,0,0,-1],[0,0,0,0,1,0]])
X2q=numpy.array([[1,0,0,0,0,0],[0,-1,0,0,0,0],[0,0,-1,0,0,0],
                 [0,0,0,1,0,0],[0,0,0,0,-1,0],[0,0,0,0,0,-1]])
X3q=numpy.array([[1,0,0,0,0,0],[0,0,1,0,0,0],[0,-1,0,0,0,0],
                 [0,0,0,1,0,0],[0,0,0,0,0,1],[0,0,0,0,-1,0]])
Y1q=numpy.array([[0,0,1,0,0,0],[0,1,0,0,0,0],[-1,0,0,0,0,0],
                 [0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,0,-1,0,0]])
Y2q=numpy.array([[-1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,-1,0,0,0],
                 [0,0,0,-1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,-1]])
Y3q=numpy.array([[0,0,-1,0,0,0],[0,1,0,0,0,0],[1,0,0,0,0,0],
                 [0,0,0,0,0,-1],[0,0,0,0,1,0],[0,0,0,1,0,0]])
Z1q=numpy.array([[0,-1,0,0,0,0],[1,0,0,0,0,0],[0,0,1,0,0,0],
                 [0,0,0,0,-1,0],[0,0,0,1,0,0],[0,0,0,0,0,1]])
Z2q=numpy.array([[-1,0,0,0,0,0],[0,-1,0,0,0,0],[0,0,1,0,0,0],
                 [0,0,0,-1,0,0],[0,0,0,0,-1,0],[0,0,0,0,0,1]])
Z3q=numpy.array([[0,1,0,0,0,0],[-1,0,0,0,0,0],[0,0,1,0,0,0],
                 [0,0,0,0,1,0],[0,0,0,-1,0,0],[0,0,0,0,0,1]])

    #shorthand for calling transformations
T={}
T[(0,1)]=X1q
T[(0,2)]=X2q
T[(0,3)]=X3q
T[(1,1)]=Y1q
T[(1,2)]=Y2q
T[(1,3)]=Y3q
T[(2,1)]=Z1q
T[(2,2)]=Z2q
T[(2,3)]=Z3q

"""
Twist operations
axis: 0,1,2 for X,Y,Z. Twist around this axis
ring:  -1 for face farthest along negative axis
        0 for middle section
        1 for face farthest along positive axis
quarters: 1,2, or 3 quarters in positive (right hand) direction
"""
#Twist of a single piece
def twistpiece(piece,axis,ring,quarters):
    if int(piece[axis])==ring:
        return T[(axis,quarters)]@piece
    
    else:
        return piece

#One twist of one ring (section) of a cube
#twist of middle section is executed as 2 twists of edge sections in the
#opposite direction.
def twistcube(cube,axis,ring,quarters):
    if ring==0:
        C=twistcube(cube,axis,-1,4-quarters)
        return twistcube(C,axis,1,4-quarters)
    else:
        return [twistpiece(piece,axis,ring,quarters) for piece in cube]

#Execute a series of twists. The series is a list of tuples. Each tuple has the 
        #axis, ring, and quarters elements. The * expands the tuple for evaluation.
def twist_series(cube,twists):
    A=cube[:]
    for twist in twists:
        A=twistcube(A,*twist)
    return A

#Compare 2 cubes to determine which pieces are in the same position and orientation
    #after a twist or twist series

#Returns 0 or 1 for same location and 0 or 1 for same orientation
def comppiece(a,b):
    return [sum([a[i]==b[i] for i in range(3)])==3,sum([a[i]==b[i] for i in range(3,6)])==3]

def compcube(cube1,cube2):
    return [comppiece(p1,p2) for p1,p2 in zip(cube1,cube2)]

def changed_pieces(cube1,cube2):
    cp=[]
    cc=compcube(cube1,cube2)
    for a,c in zip(cube1,cc):
        if not (c[0] and c[1]):
            cp.append(list(a[:3]))
    return cp

def describe_pieces(pieces):
    if any([all([p[i]==0 for p in pieces]) for i in range(3)]):
        return str(len(pieces))+ ' edges, same slice'
    elif all([0 in p for p in pieces]):
        if any([any([all([p[i]==j for p in pieces]) for i in range(3)]) for j in [-1,1]]):
            return str(len(pieces))+ ' edges, same face'
        else:
            return str(len(pieces))+ ' edges, scattered'
    else:
        return "other"
 
def finished_cube():
    start_positions=list(itertools.product([-1,0,1],repeat=3))
    for piece in start_positions[:]:
        if abs(int(piece[0]))+abs(int(piece[1]))+abs(int(piece[2]))<2:
            start_positions.remove(piece)
    return [numpy.array(list(a)+[0,1,0]) for a in start_positions]

def all_moves():
    return list(itertools.product([0,1,2],[-1,0,1],[1,2,3]))

def allRHpermutations():
    axes=[1,2,3]
    first2axes=list(itertools.permutations(axes,2))
    directions=[-1,1]
    first2d=list(itertools.product(directions,repeat=2))
    
    permutes=[]
    for ax in first2axes:
        a=ax[0]
        b=ax[1]
        s=(b-a)%3#1 for xy,yz,zx, 2 otherwise
        s=3-2*s
        for d in first2d:
            ax3=6-a-b
            c=ax3*s*d[0]*d[1]
            permutes.append((d[0]*a,d[1]*b,c))
    return permutes

def generate_random_sequence(n):
    axis=0
    ring=randint(0,1)
    quarters=randint(1,2)
    seq=[(axis,ring,quarters)]
    axis=1
    ring=randint(0,1)
    quarters=randint(1,2)
    seq.append((axis,ring,quarters))
    for i in range(n-2):
        axis=axis_offset(axis,randint(1,2))
        ring=randint(-1,1)
        quarters=randint(1,3)
        seq.append((axis,ring,quarters))
    return seq

first_twists=list(itertools.product([0],[0,1],[1,2]))
second_twists=list(itertools.product([1],[0,1],[1,2]))
third_twists=list(itertools.product([0,2],[-1,0,1],[1,2,3]))
def next_twists(a):
    axes=[0,1,2]
    axes.remove(a)
    return list(itertools.product(axes,[-1,0,1],[1,2,3]))

first_corner_twists=list(itertools.product([0],[1],[1,2]))
second_corner_twists=list(itertools.product([1],[1],[1,2]))
third_corner_twists=list(itertools.product([0,2],[-1,1],[1,2,3]))
def next_corner_twists(a):
    axes=[0,1,2]
    axes.remove(a)
    return list(itertools.product(axes,[-1,1],[1,2,3]))

def get_all_twists(n,twist_list=[]):
    if len(twist_list)>n:
        return twist_list[:]
    else:
        if n<=1:
            return [[0],first_twists]
        elif n==2:
            return [[0],first_twists,list(itertools.product(first_twists,second_twists))]
        elif n==3:
            twist_list=get_all_twists(2,twist_list)
            twist_list.append(list(itertools.product(first_twists,second_twists,third_twists)))
            return twist_list[:]
        else:
            twist_list=get_all_twists(n-1,twist_list)
            twistsn=[]
            for twists in twist_list[-1]:
                nexts=next_twists(twists[-1][0])
                for x in nexts:
                    nextn=list(twists)+[x]
                    twistsn.append(nextn)
            twist_list.append(twistsn)
        return twist_list

def get_all_corner_twists(n,ctl=[]):
    if len(ctl)>n:
        return ctl[:]
    else:
        if n<=1:
            return [[0],first_corner_twists]
        elif n==2:
            return [[0],first_corner_twists,list(itertools.product(first_corner_twists,second_corner_twists))]
        elif n==3:
            ctl=get_all_corner_twists(2,ctl)
            ctl.append(list(itertools.product(first_corner_twists,second_corner_twists,third_corner_twists)))
            return ctl
        else:
            ctl=get_all_corner_twists(n-1,ctl)
            twistsn=[]
            for twists in ctl[-1]:
                nexts=next_corner_twists(twists[-1][0])
                for x in nexts:
                    nextn=list(twists)+[x]
                    twistsn.append(nextn)
            ctl.append(twistsn)
        return ctl

def axis_offset(axis,offset):
    return (axis+offset)%3

def find_unique_rotations(moves,max_changed,attempts,Blist):
    A=finished_cube()
    ur=[]
    for att in range(attempts):
        twists=generate_random_sequence(moves)
        B=twist_series(A,twists)
        cp=changed_pieces(A,B)
        if len(cp)>0 and len(cp)<=max_changed and not any([numpy.array_equal(B,BL) for BL in Blist]):
            ur.append(twists)
            print("\r")
            print(twists)
            print(cp)
            print(describe_pieces(cp))
            for p in allRHpermutations():
                newtwists=[rotate(twist,p) for twist in twists]
                Bp=twist_series(A,newtwists)
                cpp=changed_pieces(A,Bp)
                if len(cpp)==len(cp):
                    Blist.append(Bp[:])
                else:
                    print('Error! bad permutation')
                    print(p)
                    
    return ur,Blist

def find_all_unique_rotations(moves,max_changed,Blist,twist_list):
    A=finished_cube()
    ur=[]
    for m in range(0,moves+1):
        for twists in twist_list[m]:
            B=twist_series(A,twists)
            cp=changed_pieces(A,B)
            if len(cp)>0 and len(cp)<=max_changed and not any([numpy.array_equal(B,BL) for BL in Blist]):
                ur.append(twists)
                print("\r")
                print(twists)
                print(cp)
                print(describe_pieces(cp))
                for p in allRHpermutations():
                    newtwists=[rotate(twist,p) for twist in twists]
                    Bp=twist_series(A,newtwists)
                    cpp=changed_pieces(A,Bp)
                    if len(cpp)==len(cp):
                        Blist.append(Bp[:])
                    else:
                        print('error: bad permutation')
                        print(twists)
                        print(p)
                        print(newtwists)
    return ur,Blist
            
def find_corner_only_rotations(moves,Blist=[]):
    A=finished_cube()
    ur=[]
    twistlist=get_all_twists(moves)
    for twistsm in twistlist[2:]:
        for twists in twistsm:
            B=twist_series(A,twists)
            cp=changed_pieces(A,B)
            if len(cp)>0 and cornersonly(cp) and not any([numpy.array_equal(B,BL) for BL in Blist]):
                ur.append(twists)
                print("\r")
                print(twists)
                print(cp)
                print(describe_pieces(cp))
                for p in allRHpermutations():
                    newtwists=[rotate(twist,p) for twist in twists]
                    Bp=twist_series(A,newtwists)
                    cpp=changed_pieces(A,Bp)
                    if len(cpp)==len(cp):
                        Blist.append(Bp[:])
                    else:
                        print('Error! bad permutation')
                        print(p)
                        
    return ur,Blist

#checks whether only corner pieces are in the changed pieces list
def cornersonly(cpl):
    for cp in cpl:
        if 0 in cp:
            return False
            break
    else:
        return True
    
def rotate(move,new_coords):
    ax=new_coords[move[0]]#the new rotation axis for this move
    a=abs(ax)-1#0,1,2 for X,Y,Z
    s=numpy.sign(ax)#whether axis is flipped
    return (a,s*move[1],(s*move[2])%4)