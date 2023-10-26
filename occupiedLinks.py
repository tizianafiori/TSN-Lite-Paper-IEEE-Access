import numpy as np

def occupiedLinks(paths,paths_constr,broadcastPath,flightPhase):
#def occupiedLinks():


    link = []
    link_2 = []

    if flightPhase == 3:
        pathsArray = np.array([3, 2, 3, 2, 5, 4, 1, 4, 3, 2, 3, 6, 3, 2, 3, 2, 3, 2])
    
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
