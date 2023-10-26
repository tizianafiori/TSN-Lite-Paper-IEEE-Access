from Traffic3 import *
from Traffic2 import *
from Traffic1 import *
from calcReqSlot import *
from occupiedLinks import *
import math

def loadTrafficData(flightPhase,slotDuration,bitRate,swType):

    if flightPhase == 3:
        T, o, d, linkLen, messLen, paths, broadcastPath, availab_queue, paths_constr = Traffic3()
    elif flightPhase == 2:
        T, o, d, linkLen, messLen, paths, broadcastPath,availab_queue, paths_constr = Traffic2()
    else:
        T, o, d, linkLen, messLen, paths, broadcastPath,availab_queue, paths_constr = Traffic1()

    reqSlotTSN, reqSlot_delay_medium = calcReqSlot(linkLen,messLen,paths,slotDuration,bitRate,swType)

    link,linkBinary, broadcastLink,linkBinary_Constr = occupiedLinks(paths,paths_constr, broadcastPath,flightPhase)

    Nm = len(o)
    Nl = 0

    for m  in range(Nm):
        Nl = max(Nl, max(link[m]))

    Nec = T[0]

    for i in range(len(T)-1):
        Nec = math.lcm(Nec, T[i+1])



    gamma = Nec / np.array(T)

    return T,o,d,Nm,Nl,Nec,gamma,reqSlotTSN, reqSlot_delay_medium, link,broadcastLink,linkBinary,paths,broadcastPath, availab_queue,linkBinary_Constr