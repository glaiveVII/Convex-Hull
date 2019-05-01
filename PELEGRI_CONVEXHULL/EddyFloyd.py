# -*- coding: utf-8 -*-
from itertools import permutations
from math import *
from utils import is_convex, scatter_plot, point_in_polygon
from exhaustive import exhaustive
from utils import polar_quicksort, find_min, angle, norm,determinant,distance_from_point_to_line

"""
Programme pour Eddy Floyd 
"""


#Algorithme général en O(n*log(n))

def EddyFloyd(E, show=True, save=False, detailed=False):
    g,d,E1,E2=points_max(E)
    #on coupe notre liste en deux 
    E1=point_up(E1,g,d)
    E2=point_low(E2,g,d)
    return (polar_quicksort(E1+E2,d))

#O(n)
def points_max(E):
    n=len(E)
    g,d=E[0],E[1]
    for k in range (2,n):
        if d[0]<E[k][0]:
            d=E[k]
        elif g[0]>E[k][0]:
            g=E[k]
    E1,E2=[],[]
    for k in range (n):
        if determinant(g,E[k],d)>0:
            E2.append(E[k])
        elif determinant(g,E[k],d)<0:
            E1.append(E[k])
    return g,d,E1,E2

#renvoie le point le plus haut parmi l'ensemble des points de Ei
#O(n)    
def point_up(Ei,g,d):
    #print(Ei)
    #print("\n")
    n=len(Ei)
    if n < 2 :
        return(Ei+[g]+[d])
    m=Ei[0]
    a=distance_from_point_to_line(m,[g,d])
    #permet de récupérer le point ayant l'angle max avec g et d
    for k in range(n):
        if distance_from_point_to_line(Ei[k],[g,d])>a:
            m=Ei[k]
            a=distance_from_point_to_line(Ei[k],[g,d])
    #on calcule les deux ensembles de points au dessus
    #ce sont les seuls points susceptibles d'être dans l'enveloppe convexe
    Ei1,Ei2=[],[]
    for k in range(n):
        if determinant(g,Ei[k],m)<0:
            Ei1.append(Ei[k])
        if determinant(m,Ei[k],d)<0:
            Ei2.append(Ei[k])
        
    return(point_up(Ei1,g,m)+point_up(Ei2,m,d))
    
#renvoie le point le plus bas parmi l'ensemble des points de Ei
#O(n)
def point_low(Ei,g,d):
    n=len(Ei)
    if n <2 :
        return(Ei+[g]+[d])
    m=Ei[0]
    a=distance_from_point_to_line(m,[g,d])
    #permet de récupérer le point ayant l'angle max avec g et d
    for k in range(n):
        if distance_from_point_to_line(Ei[k],[g,d])>a:
            m=Ei[k]
            a=distance_from_point_to_line(Ei[k],[g,d])
    #print(m)
    #print(" c'est m\n")
    #on calcule les deux ensembles de points au dessus
    #ce sont les seuls points susceptibles d'être dans l'enveloppe convexe
    Ei1,Ei2=[],[]
    for k in range(n):
        if determinant(g,Ei[k],m)>0:
            Ei1.append(Ei[k])
        if determinant(m,Ei[k],d)>0:
            Ei2.append(Ei[k])
    #print("Ei1" )
    #print(Ei1)
    #print("\n Ei2")
    #print(Ei2)       
    return(point_low(Ei1,g,m)+point_low(Ei2,m,d))
    
    
    
    
    