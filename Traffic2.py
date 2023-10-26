import numpy as np


def Traffic2():

    o = [0, 0, 3, 1, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0]  #Offset
    o = list(np.array(o) + 1)
    T = [1, 1, 8, 4, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1] #Period
    d = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #Deadline

    linkLen = [1.96, 1.96, 1.09, 1.09, 1.09, 1.09, 1.09, 1.09, 4.03, 4.03, 4.03, 4.03, 1.09, 1.09, 8.62, 8.62, 8.62, 8.62, 1.09, 1.09] #m
    messLen = [64.5, 64.5, 64.5, 88.5, 64.5, 64.5, 64.5, 64.5, 64.5, 64.5, 64.5, 64.5, 64.5, 64.5] #bytes

    availab_queue = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8] # number of available queues for each link

    broadcastPaths = [[3, 2, 0],
    [3, 6, 0],
    [3, 9, 12]]


    paths_constr = [[2], [9,12], [9,12], [4], [4], [10, 4], [[2], [6]], [[6,0], [9,12]],[2], [2], [2], [9,12], [9,12], [9,12]]


    paths = [[3, 2],
    [3, 9, 12],
    [3, 9, 12],
    [5, 4],
    [1, 4],
    [11, 10, 4],
    [[3, 2],[3, 6]],
    [[3, 6, 0],[3, 9,12]],
    [3, 2],
    [3, 2],
    [3, 2],
    [3, 9, 12],
    [3, 9, 12],
    [3, 9, 12]]

    return T, o, d, linkLen, messLen, paths, broadcastPaths, availab_queue, paths_constr
