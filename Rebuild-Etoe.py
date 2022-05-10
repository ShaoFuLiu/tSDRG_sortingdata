# End to end Correlation
### average raw data to meta data

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Spin = str(2)
BC = 'OBC'
M = 40
P = 10
Ls = [16,32,48,64]
# Dimer = ["Dim005","Dim010","Dim015","Dim020","Dim025","Dim030","Dim035","Dim040","Dim045","Dim050"]
Dimer = ["Dim000"]
# Jdis = ["Jdis020","Jdis040","Jdis060","Jdis080","Jdis100"]
Jdis = ["Jdis050","Jdis100","Jdis150","Jdis200","Jdis250"]
datanum = 3000
init_seed = 1

for i in range(len(Ls)):
    L = Ls[i]

    for j in range(len(Jdis)):
        jdis = Jdis[j]
        J = float(Jdis[j][4] + '.' + Jdis[j][5] + Jdis[j][6])

        for d in range(len(Dimer)):
            dfstr = pd.DataFrame(columns = ['corr', 'error', 'N'])
            dimer = Dimer[d]
            D = float(Dimer[d][3] + '.' + Dimer[d][4] + Dimer[d][5])
            x = 0
            dftc = 0
            arr = []
            N = datanum

            for k in range(datanum):
                num = str(k+init_seed)
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/corr1_etoe.csv'

                if (os.path.exists(myfile) == False): # Some data is not ok, so we need to ignore it.
                    N = N-1
                    continue

                df = pd.read_csv(myfile)
                arr.append(num) # Record the number of data that is ok.

                if(k == 0):
                    dftc = df['corr']

                dfc = df['corr']
                if(k != 0):
                    dftc += dfc

            dftc = -1*dftc  #C_1(L) = [<S_1*S_L>]_D = -1*<S_1*S_L>

            if(N == 0):
                print(str(L)+'_'+jdis+'_'+dimer+' has no data!!!')
                continue
            print(str(L)+'_'+jdis+'_'+dimer+'_'+str(N))

            dfavc = dftc/N

            for a in range(N):
                num = arr[a]
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/corr1_etoe.csv'
                df = pd.read_csv(myfile)
                x += np.square(-1*df['corr'][0]-dfavc.mean())

            if (N != 1):
                std = np.sqrt(x/(N-1))
                error = std/np.sqrt(N)
            else:
                error = 0

            mean = {'corr':dfavc.mean(), 'error':error, 'N':N}  # average
            dfstr.loc[0] = mean

            direc = '/home/liusf/tSDRG/Sorting_data/Spin'+ Spin +'/metadata/EndtoEnd/'+ jdis
            if (os.path.exists(direc) == False):
                os.mkdir(direc)
            direc2 = direc + '/' + dimer
            if (os.path.exists(direc2) == False):
                os.mkdir(direc2)
            path = direc2 +'/'+ BC +'_L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_Corr.csv'
            dfstr.to_csv(path,index=0)

print('all done')