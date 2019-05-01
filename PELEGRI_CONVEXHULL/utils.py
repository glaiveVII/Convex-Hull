import math
import time
import os
from math import atan2  # for computing polar angle
from random import randint, sample  # for sorting and creating data pts

from matplotlib import pyplot as plt  # for plotting


def create_points(num_points, minimum=-100, maximum=100):
    """
    Generates a list of fixed length of unique [x,y] coodinates as lists, where each [x,y] is chosen randomly from a
    given range.

    :param num_points: number of points to create
    :param minimum: the minimum value for xs and ys
    :param maximum: the maximum value for xs and ys
    :return: a list of unique (x,y) coordinates of length 'num_points'
    :raise: a ValueError exception if the number of points is too large for the given boundaries
    """
    delta = maximum - minimum
    if delta * delta < num_points:
        raise ValueError("Number of points too large for the available space")
    ps = sample(range(0, delta * delta), num_points)
    points = []
    for p in ps:
        points.append([(p % delta) + minimum, (p // delta) + minimum])
    return points

        
        
# Fonction pour creer des points "proche des bords" afin d'avoir l'enveloppe la plus grande possible
    #   Nous avons utiliser cette generation de point pour notre compte rendu afin de montrer que la 
    #   méthode de Jarvis est dans ce cas moins efficace ! 
def create_points_etale2(num_points, mini, maxi):
 
    # fonction pour generer des points tres etalé sur la carte et avoir un tres gorsse enveloppe convexe 
    points =[]
    
    # comme le probleme est symetrique la repartition est 
    # la meme pour tous les intervales suivant 
    for i in range(num_points):
        a = randint(1,4)
        if a == 1 :
            x = randint(mini, maxi)
            y = randint(mini, mini*0.8)
            points.append([x,y])
        if a == 2 :
            x = randint(mini, maxi)
            y = randint(0.8*maxi, maxi)
            points.append([x,y])
        if a == 3 :
            y = randint(mini, maxi)
            x = randint(mini, mini*0.8)
            points.append([x,y])
        if a == 4 :
            y = randint(mini, maxi)
            x = randint(0.8*maxi, maxi)
            points.append([x,y])

    return points
     
#l = create_points_etale2(10, 0, 10)
#print(l)

def scatter_plot(points, convex_hulls=None, all_points=[], rays=None, minimum=-100,
                 maximum=100, title="convex hull",
                 show=False, save=False, rep='./figs/', prefix='convexhull_'):
    """
    Creates a scatter plot, input is a list of [x,y] coordinates.
    The second input 'convex_hull' is a list of list of [x,y] coordinates consisting of those points in 'points' which
    make up some convex hulls.
    If not None, the elements of this list will be used to draw outer boundaries (convex hulls surrounding the data
    points).

    :param points: list of points to draw (in blue)
    :param convex_hulls: list of convex hulls to draws (in red)
    :param rays: list of rays (point pairs) to display
    :param all_points: list of other points to draw (in gray)
    :param minimum: minimum value for xs and ys
    :param maximum: maximum value for xs and ys
    :param title: title of the drawing
    :param show: if True, a windows will display the drawing (default is False)
    :param save: if True, the drawing is saved in 'rep' directory as a .png image (default is False)
    :param rep: directory to save .png images
    :param prefix: prefix for the name of the .png images (that is followed by a time stamp from :func:`time.time()
    time.time()`)
    :return: nothing
    """
    fig = plt.figure(title)
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_xlim(xmin=minimum, xmax=maximum)
    ax.set_ylim(ymin=minimum, ymax=maximum)

    if len(all_points) > 0:
        xall, yall = zip(*all_points)  # unzip into x and y coord lists
        plt.scatter(xall, yall, c='lightgray')  # plot the data points
    xs, ys = zip(*points)  # unzip into x and y coord lists
    plt.scatter(xs, ys)  # plot the data points

    if convex_hulls is not None:
        for convex_hull in convex_hulls:
            # plot the convex hull boundary, extra iteration at
            # the end so that the bounding line wraps around
            for i in range(1, len(convex_hull) + 1):
                if i == len(convex_hull):
                    i = 0  # wrap
                c0 = convex_hull[i - 1]
                c1 = convex_hull[i]
                plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
                plt.scatter((c0[0], c1[0]), (c0[1], c1[1]), c='r')
            if len(convex_hull) > 2:
                xs, ys = zip(*convex_hull)  # unzip into x and y coord lists
                plt.fill(xs, ys, 'r', alpha=0.2)

    if rays is not None:
        for ray in rays:
            for i in range(1, len(ray) + 1):
                if i == len(ray):
                    i = 0  # wrap
                c0 = ray[i - 1]
                c1 = ray[i]
                plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'darkgray', linestyle=':')
                plt.scatter((c0[0], c1[0]), (c0[1], c1[1]), c='darkgray')

    if show:
        plt.show()
    if save:
        directory = rep
        if not os.path.exists(directory):
            os.makedirs(directory)
        file = directory + prefix + repr(time.time()) + ".png"
        fig.savefig(file, bbox_inches='tight')


def point_in_polygon(point, polygon):
    """
    Determines whether a [x,y] point is strictly inside a convex polygon defined as an ordered list of [x,y] points.

    :param point: the point to check
    :param polygon: the polygon
    :return: True if point is inside polygon, False otherwise
    """
    x = point[0]
    y = point[1]
    n = len(polygon)
    inside = False
    xints = 0.0
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def polar_angle(point1, point2):
    """
    Computes the polar angle (in radians) from point1 to point2, using atan2.

    :param point1: first point coordinates as a [x,y] list
    :param point2: second point coordinates as a [x,y] list
    :return: the polar angle from p0 to p1
    """
    y_span = point1[1] - point2[1]
    x_span = point1[0] - point2[0]
    return atan2(y_span, x_span)


def distance(point1, point2):
    """
    Computes the Eclidean distance from point1 to point2.
    Square root is not applied for sake of speed.

    :param point1: first point coordinates as a [x,y] list
    :param point2: second point coordinates as a [x,y] list
    :return: squared Euclidean distance between point1 and point2
    """
    y_span = point1[1] - point2[1]
    x_span = point1[0] - point2[0]
    return y_span ** 2 + x_span ** 2


def norm(point1, point2):
    """
    Computes the 2D norm from point1 to point2.

    :param point1: first point coordinates as a [x,y] list
    :param point2: second point coordinates as a [x,y] list
    :return: the 2D norm from point1 to point2
    """
    sum(abs(a - b) for a, b in zip(point1, point2))


def distance_from_point_to_line(point, line):
    """
    Computes the distance from point to line, as defined
    in https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

    :param point: the point coordinates as a [x,y] list
    :param line: the line coordinates as a list of 2 [x,y] list
    :return: the distance
    """
    x0 = point[0]
    y0 = point[1]
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    return abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / (
            distance(line[0], line[1]) ** 2)


def determinant(point1, point2, point3):
    """
    Compute the determinant of three points, to determine the turn direction, as a 3x3 matrix:
    [p1(x) p1(y) 1]
    [p2(x) p2(y) 1]
    [p3(x) p3(y) 1]

    :param point1: the first point coordinates as a [x,y] list
    :param point2: the second point coordinates as a [x,y] list
    :param point3: the third point coordinates as a [x,y] list
    :return: a value >0 if counter-clockwise, <0 if clockwise or =0 if collinear
    """
    return (point2[0] - point1[0]) * (point3[1] - point1[1]) \
           - (point2[1] - point1[1]) * (point3[0] - point1[0])


def angle(point1, point2, point3):
    """
    Returns the angle (in radians formed) by three points. The second point is the root of the angle.

    :param point1: the first point coordinates as a [x,y] list
    :param point2: the second point coordinates as a [x,y] list
    :param point3: the third point coordinates as a [x,y] list
    :return: the angle formed by the three points in radians
    """
    return math.acos(
        (distance(point2, point1) + distance(point2, point3) - distance(point1, point3)) / (
                2 * math.sqrt(distance(point2, point1)) * math.sqrt(distance(point2, point3))))


def is_convex(points):
    """
    Determines whether a set of points constitutes a convex polygon.

    :param points: an ordered list of [x,y] points
    :return: True if the points forms a convex polygon
    """
    if len(points) == 3:
        return True
    same_sign = True
    turn = angle(points[0], points[1], points[2])
    total = 180 - math.degrees(turn)
    i = 1
    while same_sign and i < len(points):
        new_turn = angle(points[(i + 0) % len(points)],
                         points[(i + 1) % len(points)],
                         points[(i + 2) % len(points)])
        total = 180 - math.degrees(new_turn) + total
        i = i + 1
        same_sign = (new_turn * turn) >= 0
        turn = new_turn
    return i == len(points) and total <= 360


def polar_quicksort(points, anchor):
    """
    Sorts the points in order of increasing polar angle from 'anchor' point.
    For any values with equal polar angles, a second sort is applied to ensure increasing distance from the 'anchor'
    point.

    :param points: the list of [x,y] points to sort
    :param anchor: the reference point to computer polar angle
    :return: the ordered list of points
    """

    if len(points) <= 1:
        return points
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(points[randint(0, len(points) - 1)],
                          anchor)  # select random pivot
    for pt in points:
        pt_ang = polar_angle(pt, anchor)  # calculate current point angle
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return polar_quicksort(smaller, anchor) + sorted(equal, key=lambda x: distance(x, anchor)) + polar_quicksort(
        larger, anchor)


#O(n): 
    
def find_min(points): #trouve le point le plus bas
    n=len(points)
    p0=points[0]
    y=p0[1]
    x=p0[0]
    for k in range(n):
        pk=points[k]
        if y>pk[1]:
            p0=pk
            y=pk[1]
            x=pk[0]
        elif y==pk[1] and x>pk[0]:
            p0=pk
            y=pk[1]
            x=pk[0]
    return p0


# O(n) : on parcourt les points restant et on regarde lequel est le meilleur 
def prochainPoint(tab, hull,i):
    n=len(tab)
    j0=tab[0]
    angle0=polar_angle(j0,i)
    print("angle0",angle0)
    d=0
    for k in range(2,n):
        j=tab[k]
        if j!=i : 
            angle=polar_angle(j,i)
            if angle<angle0 and angle>0 and  determinant(hull[len(hull)-2],hull[len(hull)-1],j) :
                j0=j
                angle0=angle
                d=k
    del tab[d]
    return j0