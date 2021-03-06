#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import permutations
from math import *
from utils import is_convex, scatter_plot, point_in_polygon
from exhaustive import exhaustive
from utils import polar_quicksort, find_min, angle, norm,determinant
from random import randint 
from math import atan2

# ICI DEUXIEME PROGRAMME POUR SHAMOS AUTRE PSEUDO SOLUTION
"""
        Ceci est un code pour Shamos qui marche mais ne respecte pas excatement la methode 
    de Shamos qui nous a posé problème (dans quelques rare cas certains l'enveloppe convexe 
    n'est exactement la bonne).
        En effet ici pour simplifier lors de la fusion au moment de refaire le tri des deux
    enveloppes on utilise polar_quicksort pour simplifier, en effet les rares erreurs viennent 
    de l'etape de réindexation des points des enveloppes convexes.
        Le programmes marche sur tous les cas mais est moins efficace.

"""

# ici on a modifié les fonction distance et polar_angle pour plus d'efficacité
# en effet comme on sait que le point le plus en bas fera partie de l'enveloppe convexe 
# on s'en sert comme d'un pivot et on fait tout autour de lui
 #O(1)
def distance(p0,p1=False):
    """
    Computes the Eclidean distance from point1 to point2.
    Square root is not applied for sake of speed.

    :param point1: first point coordinates as a [x,y] list
    :param point2: second point coordinates as a [x,y] list
    :return: squared Euclidean distance between point1 and point2
    """
    if p1 == False: 
        p1 = point_pivot
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return y_span**2 + x_span**2

       #O(1)      
def polar_angle(p0,p1=False):
    
    """
    Computes the polar angle (in radians) from point1 to point2, using atan2.

    :param point1: first point coordinates as a [x,y] list
    :param point2: second point coordinates as a [x,y] list
    :return: the polar angle from p0 to p1
    """
    if p1 == False: 
        p1 = point_pivot
    y_span=p0[1]-p1[1]
    x_span=p0[0]-p1[0]
    return atan2(y_span,x_span)



#Algorithme utilisant le principe de l'algorithme de Graham
#Comme il prend en entrée une E liste déjà triée par angle polaire
# en fonction de son premier élément on a une complexité en O(n)

def Balayage_graham(points): 

    global point_pivot
    
    p0=points[0]
    # notre point_pivot est essentiel pour faire de scan de Graham
    # on prend celui le plus en bas et on fait tous les calculs par rapport à celui-ci 
    # car on sait que ce point sera toujours dans l'enveloppe convexe !! 
    point_pivot = points[points.index(p0)]
    #print("oojdcnflqbncsmdncqmsdnc")
    #print(points)
    #print("\n")
    #print(polar_quicksort(points,point_pivot))
    trie_points=points
    
    del points[0]
    hull=[p0,trie_points[0]]
    
    for s in trie_points[1:]:
        while determinant(hull[-2],hull[-1],s) <= 0:	
            del hull[-1] 
            if len(hull)<2: 
                break
      
        hull.append(s)
    return hull


#Algorithme général utilisant la méthode de Shamos
#Complexité : O(n*log(n))
def Shamos1(E,show,save):
        return Balayage_graham(Shamos_bis(E))

def Shamos_bis(E):
    n=len(E)
    if n<4:
        return polar_quicksort(E,find_min(E))
    else:
        E1,E2=Division(E)
        return Fusion(Shamos_bis(E1),Shamos_bis(E2))
    

    
# Algorithme permettant de diviser un ensemble de points en deux sous ensembles disjoints (de tailles similaires)
# Complexité : O(n)
def Division(E):
    n=len(E)
    E1,E2=[],[]
    k=0
    while k<n//2:
        E1.append(E[k])
        k+=1
    while k<n:
        E2.append(E[k])
        k+=1
    #print ("E1")
    #print(E1)
    #print ("\n")
    #print ("E2")
    #print(E2)
    #print ("\n")
    return E1,E2


# Algorithme permettant de fusionner deux listes triées par angle polaire par rapport à leur premier point
# et renvoyant une liste triée par angle polaire en fonction de son premier élément
# Complexité : O(n)
def Fusion(E1,E2):
    n1,n2=len(E1),len(E2)
    #on récupère les pivots des deux listes : ce sont les premiers éléments (car d'angle nul avec lui-même)
    p1,p2=E1[0],E2[0]
    if p1[0]<p2[0]:
        #on commence par chercher l'élément de E2 de plus petit angle avec p1
        m=p2
        min_a=polar_angle(m,p1)
        for k in range (n2):
            if polar_angle(E2[k],p1)<min_a:
                m=E2[k]
                min_a=polar_angle(E2[k],p1)
                #on récupère la position dans E2 de l'élément d'angle minimal avec p1
        min_i=E2.index(m)
        #on réarrange la deuxième liste pour que ses éléments soient triés par angles croissants par rapport à p1
        #pour ce faire on met le minimum m en premier et on garde le reste de
        E2=E2[min_i:]+E2[:min_i]
        #on peut maintenant fusioner les deux listes sur le même principe que le tri fusion
        #on conserve une liste trié avec un algorithme en O(n)
        E=[E1[0]]
        k=1
        l=0
        E2=polar_quicksort(E2,p1)
        while k<n1 and l<n2:
            if polar_angle(E1[k],E[0])<polar_angle(E2[l],E[0]):
                E.append(E1[k])
                k+=1
            else:
                E.append(E2[l])
                l+=1
        #on complète avec les éléments restant de la liste E1 ou E2
        while k<n1:
            E.append(E1[k])
            k+=1
        while l<n2:
            E.append(E2[l])
            l+=1
    else :
        #on commence par chercher l'élément de E1 de plus petit angle avec p2
        m=p1
        min_a=polar_angle(m,p2)
        for k in range (n1):
            if polar_angle(E1[k],p2)<min_a:
                m=E1[k]
                min_a=polar_angle(E1[k],p2)
                #on récupère la position dans E2 de l'élément d'angle minimal avec p1
        min_i=E1.index(m)
        #on réarrange la deuxième liste pour que ses éléments soient triés par angles croissants par rapport à p1
        #pour ce faire on met le minimum m en premier et on garde le reste de
        E1=E1[min_i:]+E1[:min_i]
        #on peut maintenant fusioner les deux listes sur le même principe que le tri fusion
        #on conserve une liste trié avec un algorithme en O(n)
        E=[E2[0]]
        k=0
        l=1
        E1=polar_quicksort(E1,p2)
        while k<n1 and l<n2:
            if polar_angle(E1[k],E[0])<polar_angle(E2[l],E[0]):
                E.append(E1[k])
                k+=1
            else:
                E.append(E2[l])
                l+=1
        #on complète avec les éléments restant de la liste E1 ou E2
        while k<n1:
            E.append(E1[k])
            k+=1
        while l<n2:
            E.append(E2[l])
            l+=1
    ##print(E)
    #print("\n")
    #print("azertyuio")
    #on a bien une liste E contenant tous les éléments et triée en fontion de E[0]
    return E
    
    
    
            