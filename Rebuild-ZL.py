### average raw ZL data to meta data

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

## ZL

Spin = str(2)
BC = 'PBC'
M = 40          ## For spin2, it should be 40 / For spin1, it should be 30
P = 10
Ls = [16]
Dimer = ["Dim000"]
Jdis = ["Jdis000"]
datanum = 1
init_seed = 1

for i in range(len(Ls)):
    L = Ls[i]

    for j in range(len(Jdis)):
        jdis = Jdis[j]
        J = float(Jdis[j][4] + '.' + Jdis[j][5] + Jdis[j][6])

        for d in range(len(Dimer)):
            dfstr = pd.DataFrame(columns = ['ZL', 'error', 'N'])
            dimer = Dimer[d]
            D = float(Dimer[d][3] + '.' + Dimer[d][4] + Dimer[d][5])
            x = 0
            dftc = 0
            arr = []
            N = datanum

            for k in range(datanum):
                num = str(k+init_seed)
                #myfile = '/home/liusf/tSDRG/MainDim/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m30_'+ num + '/ZL.csv'
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/ZL.csv'

                if (os.path.exists(myfile) == False): # Some data is not ok, so we need to ignore it.
                    N = N-1
                    continue

                df = pd.read_csv(myfile)
                arr.append(num) # Record the number of data that is ok.

                if(k == 0):
                    dftc = df['ZL']
                dfc = df['ZL']

                if(k != 0):
                    dftc += dfc

            if(N == 0):
                print(str(L)+'_'+jdis+'_'+dimer+' has no data!!!')
                continue
            print(str(L)+'_'+jdis+'_'+dimer+'_'+str(N))

            dfavc = dftc/N

            for a in range(N):
                num = arr[a]
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/ZL.csv'
                df = pd.read_csv(myfile)
                x += np.square(df['ZL'][0]-dfavc.mean())

            if (N != 1):
                std = np.sqrt(x/(N-1))
                error = std/np.sqrt(N)
            else:
                error = 0

            mean = {'ZL':dfavc.mean(), 'error':error, 'N':N}  # average
            dfstr.loc[0] = mean

            direc = '/home/liusf/tSDRG/Sorting_data/Spin'+ Spin +'/metadata/ZL/'+ jdis
            if (os.path.exists(direc) == False):
                os.mkdir(direc)
            direc2 = direc + '/' + dimer
            if (os.path.exists(direc2) == False):
                os.mkdir(direc2)
            path = direc2 +'/'+ BC +'_L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_ZL.csv'
            dfstr.to_csv(path,index=0)

print('all done')
