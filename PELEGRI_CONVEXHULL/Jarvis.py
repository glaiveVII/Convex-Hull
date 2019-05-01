#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import permutations
from math import *
from utils import is_convex, scatter_plot, point_in_polygon
from exhaustive import exhaustive
from utils import polar_quicksort, find_min, norm,determinant,polar_angle, prochainPoint, distance

"""
Programme pour Jarvis :
"""

#omplexité : O(log(n)*n)
def Jarvis(points,show,save):
    
    # on prend le point le plus en bas pour trier on sait qu'il sera
    # forcement dans l'enveloppe convexe
    
    # la fonction pour trouver le min est en O(n)
    a =  find_min(points)
    # fonction index tres pratiquep our recuperer la postition
    #d'un element dans une liste
    index = points.index(a)
    
    l = index
    # la liste de l'enveloppe convexe
    result = []
    result.append(a)
    
    while (True):
        q = (l + 1) % len(points)
        for i in range(len(points)):
            if i == l:
                continue
           
            #si c'est colinéaire, on prend le point le plus loin 
            d = determinant(points[l], points[i], points[q])
            if d > 0 or ( d == 0 and distance(points[i], points[l]) > distance(points[q], points[l])):
                #print("on rentre dans la boucle")
                q = i
        l = q
        if l == index:
            break
        result.append(points[q])

    return result
    
    
    
    