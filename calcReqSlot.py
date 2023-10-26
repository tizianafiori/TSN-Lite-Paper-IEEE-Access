import numpy as np
import math

def calcReqSlot(linkLen,messLength,paths2,slotDuration,bitRate,swType):




    propDelay = [item * 8 for item in messLength]
    propDelay = [item / 100 for item in propDelay]
    #reqSlotTTE = [[0 for col in range(len(messLength))] for row in range(len(linkLen))]
    reqSlotTSN = np.zeros((len(linkLen), len(messLength)))


    for m in range(len(messLength)):
        alternative = paths2[m]
        count = 0
        for elem in alternative:
            # Check if type of element is list
            if type(elem) == list:
                # Again call this function to get the size of this element
                count += len(elem)
            else:
                count += 1
        ind = count / len(alternative)

        currentDelay = [[0 for col in range(int(ind))] for row in range(1)]

        non0 = []
        currentLinks = []
        propTimeAdd = []
        currentDelay = []
        maxDelay = []
        for p in range(len(alternative)):
            propTimeAdd.clear()
            currentLinks.clear()
            currentDelay.clear()
            maxDelay.clear()



            if int(ind) == 1:
                non0 = np.nonzero(alternative)[0]
            else:
                non0 = np.nonzero(alternative[p])[0]


            for h in non0:
                if int(ind) == 1:
                    currentLinks.append(alternative[h])

                else:
                    dummy=alternative[p]
                    currentLinks.append(dummy[h])

            #print(currentLinks)

                    #currentLinks = currentLinks[h]


            for i in currentLinks:
                propTimeAdd.append((linkLen[i-1])/200)

            #print(propTimeAdd)

            if swType == 1:
                currentDelay = [item +propDelay[m] for item in propTimeAdd]
            else:
                somma = 112/bitRate + (propDelay[m]-112/bitRate)
                currentDelay = [item +somma for item in propTimeAdd]




            for s in range(int(len(currentLinks))):
                maxDelay.append(currentDelay[s])



        #print(maxDelay)
        #print(np.array(maxDelay))
        #print(slotDuration)
        #print(currentLinks)
        #print(np.array(maxDelay)/slotDuration)
        #print(np.ceil((np.array(maxDelay) / slotDuration)))
            currentLinksIndx =  [item -1 for item in currentLinks]
            reqSlotTSN[currentLinksIndx, m] = np.ceil((np.array(maxDelay) / slotDuration))



    reqSlot_delay = []
    reqSlot_delay_medium = np.array(())
    for h in range(len(linkLen)):
        reqSlot_delay.append((linkLen[h])/200)

    reqSlot_delay_medium = np.ceil(np.array(reqSlot_delay) / slotDuration)

    #reqSlot_delay_medium = reqSlot_delay_medium * 1000
    #reqSlotTSN = reqSlotTSN * 1000


    return reqSlotTSN,reqSlot_delay_medium