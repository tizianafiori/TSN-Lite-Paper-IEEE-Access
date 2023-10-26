# This is a sample Python script.
import numpy.ma

from Traffic3 import *
from Traffic2 import *
from Traffic1 import *
from calcReqSlot import *
import numpy as np
from loadTrafficData import *
from occupiedLinks import *



# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

bitrate = 100 #Mbps
slotDuration = 1 #microsec
swType = 1
flightPhase = 3


T,o,d,Nm,Nl,Nec,gamma,reqSlotTSN,reqSlot_delay_medium,link,broadcastLink,linkBinary,paths,broadcastPath,availab_queue,linkBinary_Constr = loadTrafficData(flightPhase,slotDuration,bitrate,swType)

flightPhases = np.array([1,2,3])
makespan = np.zeros((len(flightPhases),Nec))
f = np.array([])

Nl_ran = range(0,Nl)
Nm_ran = range(0,Nm)
Nec_ran = range(0,Nec)

Ec_Duration = 5000 #microsec
macro_tick = Ec_Duration/slotDuration
micro_tick = 1/macro_tick
delta_sync = 0



Delta = np.zeros((Nm,Nec))

for i in range(Nm):
    for j in range(Nec):
        if (o[i]-1)+j*T[i] <= 7:
            Delta[i,(o[i]-1)+j*T[i]]=1
        else:
            Delta[i, (o[i] - 1)] = 1


delta_link = np.zeros((Nm,Nl))




#paths_array = np.array(paths)
pathsConstr = np.array([])
pathsReconstr = []
pathsFinal = []

index_broadcast = []
value_ind = []

for i in range(Nm):
    pathsReconstr = []
    alternative = paths[i]
    count = 0
    for elem in alternative:
        # Check if type of element is list
        if type(elem) == list:
            # Again call this function to get the size of this element
            count += len(elem)
        else:
            count += 1
    ind = count / len(alternative)

    if int(ind) == 1:
        pathsFinal.append(paths[i])
    else:
        pathsConstr = np.unique(np.array(paths[i]), return_index=True)
        index_path = pathsConstr[1]
        count = 0
        a = np.array(paths[i]).flatten()
        index_final = np.sort(index_path)
        for j in range(len(pathsConstr[0])):
            pathsReconstr.append(a[index_final[j]])
        pathsFinal.append(pathsReconstr)
        index_broadcast.append(i)
        value_ind.append(ind)

from docplex.mp.model import Model

v = reqSlotTSN[0:Nl,0:Nm]
C = 5000/slotDuration
scheduling_model = Model('scheduling')

f = {(i,j): scheduling_model.integer_var(lb=(o[i]-1)*macro_tick, ub=T[i]*macro_tick+(o[i]-1)*macro_tick, name="f_{0}_{1}".format(i,j)) for i in Nm_ran for j in Nl_ran}
q = {(i,j): scheduling_model.integer_var(lb=1, ub=8, name="q_{0}_{1}".format(i,j)) for i in Nm_ran for j in Nl_ran}


for j in Nl_ran:
        for i in Nm_ran:
            for k in Nm_ran:
                if i != k:
                    hp = np.lcm(T[i], T[k])
                    alfa_ran = range(0,int(hp/T[i]))
                    beta_ran = range(0,int(hp/T[k]))
                    alfa = np.array(alfa_ran)
                    beta = np.array(beta_ran)
                    for a in alfa_ran:
                        for b in beta_ran:
                            if linkBinary[i, j]*linkBinary[k, j] != 0:
                                scheduling_model.add_constraint(scheduling_model.logical_or(f[i,j]+(o[i]-1+a*T[i])*macro_tick >= f[k,j]+(o[k]-1+b*T[k])*macro_tick+v[j,k], f[k,j]+(o[k]-1+b*T[k])*macro_tick >= f[i,j]+(o[i]-1+a*T[i])*macro_tick+v[j,i]))


for i in Nm_ran:
    link_path = paths[i]
    print(paths[i])

    if not i  in index_broadcast:
        j = 0
        while j < len(link_path)-1:

            scheduling_model.add_constraint(f[i, link_path[j+1]-1]-v[link_path[j]-1, i] >= f[i, link_path[j]-1]+delta_sync)
            j = j+1

    else:
        index_value_match = index_broadcast.index(i)
        print(int(value_ind[index_value_match]))
        for h in range(len(link_path )):

            j = 0
            while j < len(link_path[h]) - 1:
                link_path_const = link_path[h]
                if link_path_const[j + 1] == 0 or link_path_const[j] == 0:
                    j = j+1
                    continue

                scheduling_model.add_constraint(f[i, link_path_const[j + 1]-1] - v[link_path_const[j]-1, i] >= f[i, link_path_const[j]-1]+delta_sync)
                j = j + 1

for i in Nm_ran:
    for j in Nl_ran:
        f[i,j] = f[i,j]-(o[i]-1)*macro_tick



for i in Nm_ran:
    link_path_i = paths[i]
    for k in Nm_ran:
        link_path_k = paths[k]
        if i != k:
            hp = np.lcm(T[i], T[k])
            alfa_ran = range(0, int(hp / T[i]))
            beta_ran = range(0, int(hp / T[k]))
            alfa = np.array(alfa_ran)
            beta = np.array(beta_ran)
            for a in alfa_ran:
                for b in beta_ran:
                    if not i in index_broadcast and not k in index_broadcast:
                        h = 0
                        while h < len(link_path_i) :
                            g =0
                            while g < len(link_path_k):
                                if linkBinary_Constr[i, link_path_i[h]-1] * linkBinary_Constr[k, link_path_i[h]-1] != 0:
                                    #if stream_Prio[k] == stream_Prio[i]:
                                    scheduling_model.add_constraint(scheduling_model.logical_or((f[k,link_path_k[g]-1]+(o[k]-1+b*T[k])*macro_tick+delta_sync <= f[i,link_path_i[h-1]-1]+((o[i]-1+a*T[i])*macro_tick)+reqSlot_delay_medium[link_path_i[h-1]-1]), (f[i,link_path_i[h]-1]+((o[i]-1+a*T[i])*macro_tick)+delta_sync <= f[k,link_path_k[g-1]-1]+((o[k]-1+b*T[k])*macro_tick)+reqSlot_delay_medium[link_path_k[g-1]-1]), q[k,link_path_i[h]-1] != q[i,link_path_i[h]-1]))

                                g = g + 1
                            h = h+1

                    if i in index_broadcast and not k in index_broadcast:
                        index_broadcast_match_i = index_broadcast.index(i)
                        for s in range(len(link_path_i)):

                            h = 0
                            while h < len(link_path_i[s]):
                                link_path_const = link_path_i[s]
                                g = 0
                                if link_path_const[h] == 0 or link_path_const[h - 1] == 0:
                                    h = h + 1
                                    continue
                                while g < len(link_path_k):
                                    if linkBinary_Constr[i, link_path_const[h] - 1] * linkBinary_Constr[k, link_path_const[h] - 1] != 0:
                                        scheduling_model.add_constraint(scheduling_model.logical_or((f[k,link_path_k[g] - 1] + (o[k] - 1 + b *T[k]) * macro_tick + delta_sync <=f[i,link_path_const[h - 1] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) +reqSlot_delay_medium[link_path_const[h - 1] - 1]),(f[i,link_path_const[h] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) + delta_sync<= f[k,link_path_k[g - 1] - 1] + ((o[k] - 1 + b *T[k]) * macro_tick) +reqSlot_delay_medium[link_path_k[g - 1] - 1]),q[k,link_path_const[h] - 1] != q[i,link_path_const[h] - 1]))
                                    g = g + 1
                                h = h + 1

                    if k in index_broadcast and not i in index_broadcast:
                        index_broadcast_match_k = index_broadcast.index(k)
                        for s in range(len(link_path_k)):

                            h = 0
                            while h < len(link_path_i):
                                g = 0
                                while g < len(link_path_k):
                                    link_path_const = link_path_k[s]
                                    if link_path_const[g] == 0 or link_path_const[g-1] == 0:
                                        g = g + 1
                                        continue
                                    if linkBinary_Constr[i, link_path_const[g] - 1] * linkBinary_Constr[k, link_path_const[g] - 1] != 0:
                                        scheduling_model.add_constraint(scheduling_model.logical_or((f[k,link_path_const[g] - 1] + (o[k] - 1 + b *T[k]) * macro_tick + delta_sync <=f[i,link_path_i[h - 1] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) +reqSlot_delay_medium[link_path_i[h - 1] - 1]),(f[i,link_path_i[h] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) + delta_sync <= f[k,link_path_const[g - 1] - 1] + ((o[k] - 1 + b *T[k]) * macro_tick) +reqSlot_delay_medium[link_path_const[g - 1] - 1]),q[k,link_path_const[g] - 1] != q[i,link_path_const[g] - 1]))
                                    g = g + 1
                                h = h + 1

                    if i in index_broadcast and k in index_broadcast:
                        index_broadcast_match_i = index_broadcast.index(i)
                        index_broadcast_match_k = index_broadcast.index(k)
                        for s in range(len(link_path_i)):

                            h = 0
                            while h < len(link_path_i[s]):
                                link_path_const_i = link_path_i[s]
                                if link_path_const_i[h] == 0 or link_path_const_i[h - 1] == 0:
                                    h = h + 1
                                    continue
                                for t in range(len(link_path_k)):
                                    link_path_const_k = link_path_k[t]
                                    g = 0
                                    while g < len(link_path_k[t]):

                                        if link_path_const_k[g] == 0 or link_path_const_k[g-1] == 0:
                                            g = g + 1
                                            continue

                                        if linkBinary_Constr[i, link_path_const_i[h] - 1] * linkBinary_Constr[k, link_path_const_i[h] - 1] != 0:

                                            scheduling_model.add_constraint(scheduling_model.logical_or((f[k,link_path_const_k[g] - 1] + (o[k] - 1 + b *T[k]) * macro_tick + delta_sync <=f[i,link_path_const_i[h - 1] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) +reqSlot_delay_medium[link_path_const_i[h - 1] - 1]),(f[i,link_path_const_i[h] - 1] + ((o[i] - 1 + a *T[i]) * macro_tick) + delta_sync  <= f[k,link_path_const_k[g - 1] - 1] + ((o[k] - 1 + b *T[k]) * macro_tick) +reqSlot_delay_medium[link_path_const_k[g - 1] - 1]),q[k,link_path_const_i[h] - 1] != q[i,link_path_const_i[h] - 1]))
                                        g = g + 1
                                h = h + 1

scheduling_model.minimize(scheduling_model.sum(f[i,j] for i in Nm_ran for j in Nl_ran))
scheduling_model.print_information()
scheduling_model.solve()
scheduling_model.print_solution()
