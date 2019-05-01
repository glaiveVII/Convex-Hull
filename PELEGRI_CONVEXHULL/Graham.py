from itertools import permutations
from math import *
from utils import is_convex, scatter_plot, point_in_polygon
from exhaustive import exhaustive
from utils import polar_quicksort, find_min, angle, norm,determinant
from random import randint 
from math import atan2



"""
Programme pour Graham : 
    
    Petit problème qui va affecter notre programme Shamos : 
        
    A cause d'un nombre limite d'itération (venant de la recursivité générant beaucoup appels)
    Le programme desfois s'arrete avec ce message d'erreur : 
        "maximum recursion depth exceeded while calling a Python object"
            
    Nous avons essayé d'augmenter le nombre d'appels à la main (avec le module sys pour fixer
    le setmaxrecurion(....)) mais cela n'a pas marché
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


#O(n*log(n))
def Graham(points,show,save): 

    # on definit une variable global essentiel pour pouvoir choisir notre "pivot"
    # avec lequel on pour voir faire nos calculs d'angles pour faire le balayages de Graham
    global point_pivot
    
    
    p0=find_min(points)
    # notre point_pivot est essentiel pour faire le scan de Graham
    # on a choisi d'utiliser le point le plus bas. On fait tous les calculs par rapport à celui-ci 
    # on l'a choisi car on sait que ce point sera toujours dans l'enveloppe convexe !! 
    point_pivot = points[points.index(p0)]


    trie_points = quicksort(points)
    del trie_points[trie_points.index(p0)]
    # hull est la liste contenant les points de l'enveloppe convexe
    hull=[p0,trie_points[0]]
    
    for s in trie_points[1:]:
        while determinant(hull[-2],hull[-1],s) <= 0:	
            del hull[-1] 
            if len(hull)<2: 
                break
      
        hull.append(s)
    return hull



#O(n*log(n)) en moyenne et O(n^2) dans le pire des cas 
def quicksort(l):
    if len(l)<=1: 
        return l
    # on fait les listes pour placer les elements autour de notre pivot
    l_inferieur= []
    l_egal = []
    l_superieur = []
    
    #on choisit le pivot de facon aleatoire et arbitraire 
    y=polar_angle(l[randint(0,len(l)-1)]) 
    
    for i in l:
        #on calcul l'angle et on l'ajoute a la liste correspondante
        x=polar_angle(i) 
        if   x < y:  
            l_inferieur.append(i)
        elif x == y: 
            l_egal.append(i)
        else: 
            l_superieur.append(i)
        
    return quicksort(l_inferieur) +quicksort(l_egal) + quicksort(l_superieur)      
            
            
