# Bulk Correlation
### average raw data to meta data

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Spin = str(2)
BC = 'PBC'
M = 40
P = 10
Ls = [16,32,48]
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
            dfstr = pd.DataFrame(columns = ['x2-x1', 'corr', 'error'])
            dimer = Dimer[d]
            D = float(Dimer[d][3] + '.' + Dimer[d][4] + Dimer[d][5])
            x = 0
            dftc = 0
            N = datanum

            for k in range(datanum):
                num = str(k+init_seed)
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_'+ num +'_corr1.csv'

                if (os.path.exists(myfile) == False): # Some data is not ok, so we need to ignore it.
                    N = N-1
                    continue

                df = pd.read_csv(myfile)
                dfr = df['x2'] - df['x1']
                DataColle = {'x2-x1': dfr}
                dfR = pd.DataFrame(DataColle, columns=['x2-x1'])

                if(k == 0):
                    dftc = df['corr']

                dfc = df['corr']
                if(k != 0):
                    dftc += dfc

            if(N == 0):
                print(str(L)+'_'+jdis+'_'+dimer+' has no data!!!')
                continue
            print(str(L)+'_'+jdis+'_'+dimer+'_'+str(N))

            for j in range(len(dftc)):  #Cb(r) = [(−1)^r·Si· Si+r⟩]
                dftc[j] = pow(-1,dfr[j])*dftc[j]

            dfavc = dftc/N
            dfavc = pd.concat([dfR,dfavc],axis=1)

            for dist in range(int(L/2)):
                r = dist+1
                dfsr = dfavc.loc[dfavc['x2-x1'] == r]
                mean = {'x2-x1':r, 'corr': dfsr['corr'].mean(), 'error': dfsr['corr'].sem()}
                dfstr.loc[dist] = mean

            direc = '/home/liusf/tSDRG/Sorting_data/Spin'+ Spin +'/metadata/Corr/'+ jdis
            if (os.path.exists(direc) == False):
                os.mkdir(direc)
            direc2 = direc + '/' + dimer
            if (os.path.exists(direc2) == False):
                os.mkdir(direc2)
            path = direc2 +'/'+ BC +'_L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_Corr.csv'
            dfstr.to_csv(path,index=0)

print('all done')