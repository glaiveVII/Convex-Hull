from random import seed
from time import time

from exhaustive import exhaustive
from utils import *
from EddyFloyd import EddyFloyd
from Jarvis import Jarvis
from Graham import Graham
from Shamos import Shamos
from Shamos1 import Shamos1






def benchmark(sizes=(10, 100, 1000, 10000, 100000), runs=100, method=EddyFloyd):
    """
    For each size in the 'sizes' list, compute the average time over a given number of runs to find the convex hull
    for a dataset of that size,
    the range used for max and min for the create_points function is always 10 times the highest value in the 'sizes'
    list.

    :param sizes: list of problem sizes to consider (default is (10, 100, 1000, 10000, 100000))
    :param method: the name of the algorithm to use (default is exhaustive)
    :param runs: the number of repetition to perform for computing average (default is 100)
    :return: nothing
    """
    print(method.__name__)
    #for s in sizes:
    s=sizes
    tot = 0.0
    print(runs)
    save=False
    show =True
    for k in range(runs):

        points = create_points(s, -100,100)
        
        # pour generer les points "étalé" pour la méthode de Jarvis
        #points = create_points_etale2(s, -100, 100)
        t0 = time.time()
        method(points, False,save=save)
        tot += (time.time() - t0)
            
    scatter_plot(points, [[]], title="convex hull : initial set", show=show, save=save)
    print("Points:", points)
    # compute the hull
    hull = method(points, show=show, save=save)
    print("Hull:", hull)
    scatter_plot(points, [hull], title="convex hull : final result", show=True, save=save)

        
    print("le temps d'exécution vaut\n")
    print(tot/runs)
    #on a le temps en seconde 
    #print("Nbre de point %d temps moyen : %0.5f" % (s, (tot/ runs)*1000))




def main():
    """
    A sample main program.

    :return: nothing
    """
    seed(0)
    #algorithms = [EddyFloyd]  # [graham, jarvis, shamos]

    #for algorithm in algorithms:
        #benchmark(sizes=range(2, 10000, 500), runs=100, method=algorithm)
        
    # POUR LES TESTS JE CHANGEAIS LE NOMBRE DE POINTS POUR CHAQUE METHODE EN ESSAYANT DE FAIRE 
    # LE PLUS DE RUN DANS LA MESURE DU POSSIBLE 
    benchmark(sizes=(1000), runs=1000, method = Jarvis)
    

if __name__ == "__main__":
    main()
