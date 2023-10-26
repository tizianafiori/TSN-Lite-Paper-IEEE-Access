import numpy as np

def occupiedLinks(paths,paths_constr,broadcastPath,flightPhase):
#def occupiedLinks():


    link = []
    link_2 = []
    #pathsArray = np.array(paths)
    #for h in range(len(pathsArray)*10):
        #pathsArray = np.hstack(pathsArray)
        #print(pathsArray)
    if flightPhase == 3:
        pathsArray = np.array([3, 2, 3, 2, 5, 4, 1, 4, 3, 2, 3, 6, 3, 2, 3, 2, 3, 2])
    elif flightPhase == 2:
        pathsArray = np.array([3, 2, 3, 9, 12,3, 9, 12,5, 4,1, 4,11, 10, 4,3, 2, 3, 6,3, 6, 0, 3, 9, 12,3, 2,3, 2,3, 2,3, 9, 12,3, 9, 12,3, 9, 12])
    else:
        pathsArray = np.array([3, 2,3, 9, 12,3, 9, 15, 18,3, 9, 15, 18,5, 4,1, 4,11, 10, 4,17, 16, 10, 4,3, 2,3,6,3, 9, 12,3, 6, 0,3, 9, 15, 18,3, 6, 0, 0,3, 2,3, 2,3, 2,3, 9, 12,3, 9, 12,3, 9, 12,3, 9, 15, 18,3, 9, 15, 18,3, 9, 15, 18])
    col = pathsArray.max()
    print(col)
    linkBinary = np.zeros((len(paths), col))
    linkBinary_Constr = np.zeros((len(paths), col))

    for m in range(len(paths)):
        alternative = np.array(paths[m])
        index = []
        index = alternative.any()
        link.append(np.unique(alternative[index]))
        linkBinary[m, np.unique(alternative[index])-1] = 1

        alternative_2 = np.array(paths_constr[m])
        index_2 = []
        index_2 = alternative_2.any()
        print(type(index_2))
        link_2.append(np.unique(alternative_2[index_2]))
        linkBinary_Constr[m, np.unique(alternative_2[index_2]) - 1] = 1




    broadcastLink = np.unique(np.array(broadcastPath))

    return link,linkBinary,broadcastLink,linkBinary_Constr
