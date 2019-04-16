#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrateur
#
# Created:     01/12/2018
# Copyright:   (c) Administrateur 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os

file_graph = 'graph_TP3.txt'

TheGraph = open(file_graph,'r')
all_arcs = TheGraph.readlines()
TheGraph.close()

Origine = []
Destination = []
MinCapacity = []
MaxCapacity = []
Cost = []

for one_arc in all_arcs:
    this_arc = one_arc.split('\t')
    orig = int(this_arc[0])
    dest = int(this_arc[1])
    mincap = int(this_arc[2])
    maxcap = int(this_arc[3])
    cost = int(this_arc[4].strip("\n"))
    Origine.append(orig)
    Destination.append(dest)
    MinCapacity.append(mincap)
    MaxCapacity.append(maxcap)
    Cost.append(cost)

NbArcs = len(Origine)
NbVertices = max(max(Origine),max(Destination))+1

print("Origine = ",Origine)
print("Destination = ",Destination)
print("MinCapacity = ",MinCapacity)
print("MaxCapacity = ",MaxCapacity)
print("Cost =",Cost)

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

Color = ['u'for j in range(0, NbArcs)]
Flow = [0 for j in range(0, NbArcs)]
Theta = [0 for j in range(0, NbArcs)]
Distance = [0 for j in range(0,NbArcs)]
The_Chain = []
'''
Marked = [False for j in range(0, NbVertices)]
Predecesseur = [-1 for j in range(0, NbVertices)]
Successeur = [-1 for j in range(0, NbVertices)]

mu_plus=[]
mu_minus=[]
'''
def SearchChainColor(u):
    global Marked
    global Predecesseur
    global Successeur

    arr = Origine[u]
    dep = Destination[u]
    In_Stack = [False for j in range(0,NbVertices)]
    print ('Search chain color: ', dep, ' to ', arr)
    opposite = {'g':'b','b':'g','u':'u'}
    List = []
    List.append(dep)
    found = False
    while (List != []) and not found:
        i = List[0]
        Marked[i] = True

        del (List[0])
        for j in range(_asucc[i],_asucc[i+1]):
            the_succ = _bsucc[j]
            the_arc= _nsucc[j]
            if ( the_succ == arr )and (Color[the_arc] in [Color[u],'r']):
                found = True
            if (not In_Stack[the_succ]) and (not Marked[the_succ]) and (Color[the_arc] in [Color[u],'r']):
                List.append(the_succ)
                In_Stack[the_succ] = True
                Predecesseur[the_succ] = i
        for j in range(_aprec[i],_aprec[i+1]):
            the_prec = _bprec[j]
            the_arc= _nprec[j]
            if ( the_prec == arr )and (Color[the_arc] in [opposite[Color[u]],'r']) and (the_arc != u):
                found = True
            if (not In_Stack[the_prec]) and (the_arc != u) and (not Marked[the_prec]) and (Color[the_arc] in [opposite[Color[u]],'r']):
                List.append(the_prec)
                In_Stack[the_prec] = True
                Successeur[the_prec] = i
    print("color",Color)
    print("found",found)
    return found

def IdentifyChain(u):
    global The_chain    #!!! by charles
    global mu_plus
    global mu_minus
    global Predecesseur
    global Successeur
    dest=Origine[u]
    orig=Destination[u]
    i=dest
    mu_plus.append(u)   #!!! by charles
    while (i != orig):
        if(Predecesseur[i] != -1):
            k=_aprec[i]
            ind = _aprec[i]+_bprec[_aprec[i]:_aprec[i+1]].index(Predecesseur[i])
            if Color[u]=='b':
                mu_plus.append(_nprec[ind])
            else:
                mu_minus.append(_nprec[ind])
            The_Chain.append(_nprec[ind]) #!!! by charles
            i=Predecesseur[i]
        elif Successeur[i] != -1:
            k = _asucc[i]
            ind = _asucc[i]+_bsucc[_asucc[i]:_asucc[i+1]].index(Successeur[i])
            if Color[u]=='b':
                mu_minus.append(_nsucc[ind])
            else:
                mu_plus.append(_nsucc[ind])
            The_Chain.append(_nsucc[ind]) #!!!  by charles
            i=Successeur[i]
    The_Chain.append(u)  #!!!  by charles
    print("mu_minus",mu_minus)
    print("mu_plus",mu_plus)
    print("The-Chain",The_Chain)
    return()


#update color for flow cout minimum
def NewUpdateColors(u):
    if (Flow[u] > MinCapacity[u] and Flow[u] < MaxCapacity[u]):
        if (Theta[u] == Cost[u]):
            col = 'r'
        if (Theta[u] < Cost[u]):
            col = 'g'
        if (Theta[u] > Cost[u]):
            col = 'b'
    elif (Flow[u] == MinCapacity[u]):
        if (Theta[u] >= Cost[u]):
            col = 'b'
        if (Theta[u] < Cost[u]):
            col = 'u'
    elif (Flow[u] == MaxCapacity[u]):
        if (Theta[u] <= Cost[u]):
            col = 'g'
        if (Theta[u] > Cost[u]):
            col = 'u'
    else:
        col = 'u'
    return (col)

#compute total distance for flot cout minimum
def NewTotalDistance():
    global Distance
    for u in range(0,NbArcs):
        if (Flow[u] < MaxCapacity[u] and Flow[u] > MinCapacity[u]):
            if (Theta[u] > Cost[u]):
                Distance[u] = (MaxCapacity[u]-Flow[u]) * (Theta[u]-Cost[u])
            if (Theta[u] < Cost[u]):
                Distance[u] = (Flow[u]-MinCapacity[u]) * (Cost[u]-Theta[u])
            if (Theta[u] == Cost[u]):
                Distance[u] = 0
        if (Flow[u] == MaxCapacity[u] or Flow[u] == MinCapacity[u]):
            Distance[u] = 0
        '''
        if (Flow[u] > MaxCapacity[u]):
            Distance[u] = Flow[u] - MaxCapacity[u]
        if (Flow[u] < MinCapacity[u]):
            Distance[u] = MinCapacity[u] - Flow[u]
        '''
        #Total = Total + Distance[u]
    return sum(Distance)
'''
def ComputeEpsilon1():
    global Flow
    episilon = 999999
    for u in mu_plus:
        print("u=",u)
        episilon = min(episilon, MaxCapacity[u] - Flow[u])
        #Flow[u] = Flow[u] + episilon

    for u in mu_minus:
        episilon = min(episilon, Flow[u] - MinCapacity[u])
        #Flow[u] = Flow[u] - episilon
'''
#update color for flot compatible
def UpdateColor(u):
        if (Flow[u] > MinCapacity[u] and Flow[u] < MaxCapacity[u]):
            col = 'r'
        if (Flow[u] <= MinCapacity[u]):
            col = 'b'
        if (Flow[u] >= MaxCapacity[u]):
            col = 'g'
        return (col)

#compute et update total distance
def TotalDistance():
    global Distance
    #Total = 0
    for u in range(0,NbArcs):
        if (Flow[u] <= MaxCapacity[u] and Flow[u] >= MinCapacity[u]):
            Distance[u] = 0
        if (Flow[u] > MaxCapacity[u]):
            Distance[u] = Flow[u] - MaxCapacity[u]
        if (Flow[u] < MinCapacity[u]):
            Distance[u] = MinCapacity[u] - Flow[u]
        #Total = Total + Distance[u]
    return sum(Distance)


#computeEpisilon pour flot compatible
def ComputeEpsilon():
    global Flow
    episilon = 999999
    for u in mu_plus:
        print("u=",u)
        episilon = min(episilon, MaxCapacity[u] - Flow[u])
    for u in mu_minus:
        print("u=",u)
        episilon = min(episilon, Flow[u] - MinCapacity[u])
    print("episilon=",episilon)
    for u in mu_plus:
        Flow[u] = Flow[u] + episilon
    for u in mu_minus:
        Flow[u] = Flow[u] - episilon


#flow compatible
for u in range(0, NbArcs):
    Color[u]=UpdateColor(u)

feasible_flow = True
while(TotalDistance()>0 and feasible_flow):
    u = Distance.index(max(Distance))
    print("Distance = ",Distance)
    print("max u=",u)
    Marked = [False for j in range(0, NbVertices)]
    Predecesseur = [-1 for j in range(0, NbVertices)]
    Successeur = [-1 for j in range(0, NbVertices)]
    The_Chain = []
    mu_plus=[]
    mu_minus=[]
    print("flow =",Flow)
    if(SearchChainColor(u)):
        IdentifyChain(u)
        ComputeEpsilon()
        for u in The_Chain:
            Color[u]=UpdateColor(u)
    else:
        feasible_flow = False

print("Compatible",feasible_flow)
print("Flow",Flow)


#Flow cout minimum
'''
for u in range(0, NbArcs):
    Color[u]=NewUpdateColors(u)

fini = True
while(NewTotalDistance()>0 and fini):
    u = Distance.index(max(Distance))
    print("Distance=",Distance)
    Marked = [False for j in range(0, NbVertices)]
    Predecesseur = [-1 for j in range(0, NbVertices)]
    Successeur = [-1 for j in range(0, NbVertices)]
    The_Chain = []
    setA=[]
    mu_plus=[]
    mu_minus=[]
    omega_plus=[]
    omega_minus=[]
    if(SearchChainColor(u)):
        IdentifyChain(u)
        print("mu_plus = ",mu_plus)
        print("mu_minus =",mu_minus)
        episilon = 999999
        for u in mu_plus:
            episilon = min(episilon, MaxCapacity[u] - Flow[u])
        for u in mu_minus:
            episilon = min(episilon, Flow[u] - MinCapacity[u])
        print("Episilon =",episilon)
        for u in mu_plus:
            Flow[u] = Flow[u] + episilon
            Color[u] = NewUpdateColors(u)
        for u in mu_minus:
            Flow[u] = Flow[u] - episilon
            Color[u] = NewUpdateColors(u)
        print("color =",Color)
        print("Flow",Flow)
        print("Theta",Theta)
    else:
        fini = False

        for u in omega_plus:
            episilon = min(episilon, MaxCapacity[u] - Flow[u])
        for u in omega_minus:
            episilon = min(episilon, Flow[u] - MinCapacity[u])
        for u in omega_plus:
            Theta[u] = Theta[u] + episilon
            Color[u] = NewUpdateColors(u)
        for u in omega_minus:
            Theta[u] = Theta[u] - episilon
            Color[u] = NewUpdateColors(u)
'''