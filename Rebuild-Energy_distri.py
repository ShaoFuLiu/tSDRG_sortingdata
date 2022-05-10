# energy distribution

import os
import math
import pandas as pd
import numpy as np

Spin = str(2)
BC = 'OBC'
M = 40
P = 10
Ls = [16,32,48]
Dimer = ["Dim000"]
Jdis = ["Jdis050","Jdis100","Jdis150","Jdis200","Jdis250"]
datanum = 100
init_seed = 1

for i in range(len(Ls)):
    L = Ls[i]

    for j in range(len(Jdis)):
        jdis = Jdis[j]
        J = float(Jdis[j][4] + '.' + Jdis[j][5] + Jdis[j][6])

        for d in range(len(Dimer)):
            dimer = Dimer[d]
            D = float(Dimer[d][3] + '.' + Dimer[d][4] + Dimer[d][5])
            df = pd.DataFrame()
            N = datanum

            for k in range(datanum):
                num = str(k+init_seed)
                myfile = '/home/liusf/tSDRG/'+ Spin +'_MainDimZL/data2/'+ BC +'/'+ jdis + '/'+ dimer + '/L'+ str(L) +'_P'+ str(P) +'_m'+ str(M) +'_'+ num + '/energy.csv'
                if (os.path.exists(myfile) == False): # Some data is not ok, so we need to ignore it.
                    N -= 1
                    continue

                df1 = pd.read_csv(myfile)
                df2 = df1[1:].reset_index()
                df1 = df1[:len(df1['energy'])-1]
                df1['energy'] = abs(df2['energy'] - df1['energy'])
                df1 = df1[df1['energy'] != 0].reset_index()

                if (k == 0):
                    df = df1
                else:
                    df = pd.concat([df, df1], ignore_index=True)

            if(N == 0):
                print(str(L)+'_'+jdis+'_'+dimer+' has no data!!!')
                continue
            print(str(L)+'_'+jdis+'_'+dimer+'_'+str(N))

            df['energy'] = np.log(df['energy'])
            direc = '/home/liusf/tSDRG/Sorting_data/Spin'+ Spin +'/metadata/Energy_gap/'+ jdis
            if (os.path.exists(direc) == False):
                os.mkdir(direc)
            direc2 = direc + '/' + dimer
            if (os.path.exists(direc2) == False):
                os.mkdir(direc2)
            path = direc2 +'/'+ BC +'_L'+ str(L) +'_P' + str(P) + '_m'+ str(M) +'_Gap_'+ str(datanum) +'.csv'
            df.to_csv(path,index=0)

print('all done')