from random import seed
import time
from Jarvis import Jarvis
from Graham import Graham
from EddyFloyd import EddyFloyd
from Shamos import Shamos
from Shamos1 import Shamos1



from exhaustive import exhaustive
from utils import create_points, scatter_plot


def main():
    """
    A sample main program to test our algorithms.

    @return: None
    """
    t0=time.time()
    # initialize the random generator seed to always use the same set of points
    seed(0)
    # creates some points
    pts = create_points(30)
  
            
    show = True  # to display a frame
    save = False  # to save into .png files in "figs" directory
    scatter_plot(pts, [[]], title="convex hull : initial set", show=show, save=save)
    print("Points:", pts)
    # compute the hull
    hull = Graham(pts, show=show, save=save)
    print("Hull:", hull)
    scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)
    t1 = time.time()
    print("temps en secondes :")
    print(t1-t0)


if __name__ == "__main__":
    main()