#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrateur
#
# Created:     21/11/2018
# Copyright:   (c) Administrateur 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os

file_graph = 'graph_TP1.txt'
#file_graph = 'test.txt'
TheGraph = open(file_graph,'r')
all_arcs = TheGraph.readlines()
TheGraph.close()

print("all_arcs: ",all_arcs)

Origine = []
Destination = []
for one_arc in all_arcs:
    this_arc = one_arc.split('\t')
    orig = int(this_arc[0])
    dest = int(this_arc[1].strip("\n"))
    Origine.append(orig)
    Destination.append(dest)

NbArcs = len(Origine)
NbVertices = max(max(Origine),max(Destination))+1

print("NbArcs = ",NbArcs)
print("NbVertices = ",NbVertices)
print("Origine = ",Origine)
print("Destination = ",Destination)

succ=[[] for i in range (NbVertices)]
prec=[[] for i in range (NbVertices)]
numsucc=[[]for i in range (NbVertices)]
numprec=[[]for i in range (NbVertices)]

for u in range(0,NbArcs):
    i = Origine[u]
    j = Destination[u]
    succ[i].append(j)
    numsucc[i].append(u)
    prec[j].append(i)
    numprec[j].append(u)

print("succ = ",succ)
print("prec = ",prec)
print("numsucc = ",numsucc)
print("numprec = ",numprec)

_asucc = []
_bsucc = []
_nsucc = []
_aprec = []
_bprec = []
_nprec = []

_is = 0
for j in range (0,NbVertices):
    _asucc.append(_is)
    _is = _is + len(succ[j])
    _bsucc = _bsucc + succ[j]
    _nsucc = _nsucc + numsucc[j]
_asucc.append(_is)

_is = 0
for j in range (0,NbVertices):
    _aprec.append(_is)
    _is = _is + len(prec[j])
    _bprec = _bprec + prec[j]
    _nprec = _nprec + numprec[j]
_aprec.append(_is)

print("_asucc = ",_asucc)
print("_bsucc = ",_bsucc)
print("_nsucc = ",_nsucc)
print("_aprec = ",_aprec)
print("_bprec = ",_bprec)
print("_nprec = ",_nprec)

def SearchChain(dep,arr):
    global Marked
    global Predecesseur
    global Successeur
    print ('Search chain : ', dep, ' to ', arr)
    List = []
    List.append(dep)
    In_Stack = [False for j in range(0,NbVertices)]
    found = False
    while (List != []) and not found:
        j = List[0]
        Marked[j] = True
        del (List[0])
        for k in succ[j]:
            if k == arr:
                found = True
            if Marked[k] == 0 and In_Stack[k] == False:
                List.append(k)
                Predecesseur[k] = j
                In_Stack[k] = True
        for d in prec[j]:
            if d == arr:
                found = True
            if Marked[d] == 0 and In_Stack[d] == False:
                List.append(d)
                Successeur[d] = j
                In_Stack[d] = True
    return found

def SearchChain_ts(u):
    global Marked
    global Predecesseur
    global Successeur
    ArcList =[]
    arr = Origine[u]
    dep = Destination[u]
    print ('Search chain : ', dep, ' to ', arr)
    List = []
    List.append(dep)
    In_Stack = [False for j in range(0,NbVertices)]
    found = False
    while (List != []) and not found:
        i = List[0]
        Marked[i] = True
        In_Stack[dep]=True
        del (List[0])
        for j in range(0,_asucc[i+1]-_asucc[i]):
            the_succ = _bsucc[_asucc[i]+j]
            the_arc= _nsucc[_asucc[i]+j]
            if( the_arc != u):
                if( the_succ == arr):
                    found = True
                if( not In_Stack[the_succ]):
                    List.append(the_succ)
                    In_Stack[the_succ] = True
                    Predecesseur[the_succ] = i
                    ArcList.append(the_arc)

        for j in range(0,_aprec[i+1]-_aprec[i]):
            the_prec = _bprec[_aprec[i]+j]
            the_arc= _nprec[_aprec[i]+j]
            if( the_arc != u):
                if( the_prec == arr):
                    found = True
                if( not In_Stack[the_prec]):
                    List.append(the_prec)
                    In_Stack[the_prec] = True
                    Successeur[the_prec] = i
                    ArcList.append(the_arc)
    print("Arclist = ",ArcList)
    print("In_Stack = ",In_Stack)
    return found


def IdentifyChain(u):
    global The_chain
    global mu_plus
    global mu_minus
    dest=Origine[u]
    orig=Destination[u]
    print("dest =",dest)
    print("orig =",orig)
    i=dest
    while (i != orig):
        if(Predecesseur[i]!=-1):
            k=Predecesseur[i]
            for j in range(0,_aprec[i+1]-_aprec[i]):
                if(_bprec[_aprec[i]+j]==k):
                    The_chain.append(_nprec[_aprec[i]+j])
                    mu_plus.append(_nprec[_aprec[i]+j])
            i=Predecesseur[i]
        if(Successeur[i]!=-1):
            k=Successeur[i]
            for j in range(0,_asucc[i+1]-_asucc[i]):
                if(_bsucc[_asucc[i]+j]==k):
                    The_chain.append(_nsucc[_asucc[i]+j])
                    mu_minus.append(_nsucc[_asucc[i]+j])
            i=Successeur[i]


Marked = [False for j in range(0, NbVertices)]
Predecesseur = [-1 for j in range(0, NbVertices)]
Successeur = [-1 for j in range(0, NbVertices)]

The_chain=[]
mu_plus=[]
mu_minus=[]
'''
while (1):
    orig = int(input("entrez le sommet origin "))
    if orig >= 0 and orig <= NbVertices - 1:
        break
while (1):
    dest = int(input("entrez le sommet destination "))
    if dest >= 0 and dest <= NbVertices - 1:
        break
'''

'''
if SearchChain(orig, dest):
    print("Found")
else:
    print("Not found")

vertex = dest
print("Chain =  ")
while (1):
    if (Predecesseur[vertex] != -1):
        print ('(', Predecesseur[vertex], vertex, ')')
        vertex = Predecesseur[vertex]
    elif (Successeur[vertex] != -1):
        print ('(', vertex, Successeur[vertex], ')')
        vertex = Successeur[vertex]
    if vertex == orig:
        break
'''

u=1
if SearchChain_ts(u):
    print("Predecesseur = ",Predecesseur)
    print("Successeur = ",Successeur)
    print("Found")
    IdentifyChain(u)
    print("The_chain = ",The_chain)
    print("mu_plus = ",mu_plus)
    print("mu_minus = ",mu_minus)
else:
    print("Not found")



