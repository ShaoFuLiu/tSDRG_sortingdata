### average raw Oz data to meta data

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

## Oz

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
            dfstr = pd.DataFrame(columns = ['O^z', 'error','N','total_data'])
            dimer = Dimer[d]
            D = float(Dimer[d][3] + '.' + Dimer[d][4] + Dimer[d][5])
            x = 0
            dftc = 0
            arr = []
            N = datanum

            for k in range(datanum):
                num = str(k+init_seed)
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num +'_string.csv'

                if (os.path.exists(myfile) == False): # Some data is not ok, so we need to ignore it.
                    print(myfile + ' does not exist!!!')
                    N = N-1
                    continue

                df = pd.read_csv(myfile)
                arr.append(num)                       # Record the number of data that is ok

                dfc = df['corr']
                if(k == 0):
                    dftc = df['corr']
                else:
                    dftc += dfc

            if(N == 0):
                print(str(L)+'_'+jdis+'_'+dimer+' has no data!!!')
                continue
            print(str(L)+'_'+jdis+'_'+dimer+'_'+str(N))

            dfavc = dftc/N                          # first average(N times)
            total_data = 0                          # real data number we have
            for m in range(len(arr)):               # Calculate error
                num = arr[m]
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num +'_string.csv'
                df = pd.read_csv(myfile)
                for l in range(df.shape[0]):
                    x += np.square(df['corr'][l]-dfavc.mean())
                total_data += df.shape[0]

            std = np.sqrt(x/(total_data-1))
            error = std/np.sqrt(total_data)
            mean = {'O^z':dfavc.mean(), 'error':error, 'N':N, 'total_data': total_data}  # second average(L/2 times)
            dfstr.loc[0] = mean

            direc = '/home/liusf/tSDRG/Sorting_data/Spin'+ Spin +'/metadata/SOP/'+ jdis
            if (os.path.exists(direc) == False):
                os.mkdir(direc)
            direc2 = direc + '/' + dimer
            if (os.path.exists(direc2) == False):
                os.mkdir(direc2)
            path = direc2 +'/'+ BC +'_L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_SOP.csv'
            dfstr.to_csv(path,index=0)

print('all done')

