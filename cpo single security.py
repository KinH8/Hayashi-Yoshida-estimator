# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:43:27 2022

@author: Wu
"""

import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import itertools


def pivot_f(name, lag=0):
    data  = pd.read_csv(name+'.csv', parse_dates=True, index_col='Dates')
    data = data[data['Price']!=0]
    data = data[data['Type']!='TRADE']
    
    data['Value'] = data['Price'] * data['Size']
    
    table  = pd.pivot_table(data, index='Dates',values=['Value','Size'],columns='Type', aggfunc=np.sum) #meta

    # Volume weighted average price
    table = table['Value'].div(table['Size'], axis=1, level=1)
    
    # Exclude pre opening period between 2 and 2.30pm
    table = table.loc[(table.index<pd.Timestamp(2022, 2, 20, 12,30,0)) | (table.index>pd.Timestamp(2022, 2, 20, 14,30,0))]

    # Exclude situation where bid > ask
    table = table.mask(table['BID']>table['ASK'], np.nan)

    temp = table.dropna().mean(axis=1).rename(name).to_frame()
    temp = temp.mask(temp.pct_change()==0,np.nan)

    temp = temp.dropna()
    temp.index = temp.index + datetime.timedelta(seconds=lag)

    return temp.pct_change()

def trade(name, lag=0):
    data  = pd.read_csv(name+'.csv', parse_dates=True, index_col='Dates')
    data = data[data['Price']!=0]
    data = data[data['Type']=='TRADE']
    
    data['Value'] = data['Price'] * data['Size']
    
    table = data.groupby(by='Dates').sum()
    
    table = table['Value']/table['Size']

    # Exclude pre opening period between 2 and 2.30pm
    table = table.loc[(table.index<pd.Timestamp(2022, 2, 21, 12,30,0)) | (table.index>pd.Timestamp(2022, 2, 21, 14,30,0))]

    temp = table.rename(name).to_frame().dropna()
    temp = temp.mask(temp.pct_change()==0,np.nan)

    temp = temp.dropna()
    temp.index = temp.index + datetime.timedelta(seconds=lag)

    return temp.pct_change()

KO3 = pivot_f('KO3 20220222')
I3 = pd.IntervalIndex.from_arrays(KO3.index[:-1], KO3.index[1:])

x=[]
y=[]

for g in np.arange(-20,21,1):
    #KO4 = pivot_f('KO1 20220222', int(g))
    KO4 = pivot_f('KO4 20220222', int(g))
    #KO4 = KO4- KO4.mean()
    I4 = pd.IntervalIndex.from_arrays(KO4.index[:-1], KO4.index[1:])
    
    
    temp = KO4[1:].values.T
    m = [I4.overlaps(i) for i in I3]
    
    df = np.array([np.multiply(temp,i).flatten() for i in m])
    
    q = np.array(KO3[1:].values)
    
    covar = 0
    for i,j in zip(q,df):
        covar += np.sum(i*j)
    
    KO3_var = np.sum(np.square(KO3))
    KO4_var = np.sum(np.square(KO4))
    p = covar / np.sqrt(KO3_var.values * KO4_var.values)
    x.append(g)
    y.append(p)
    #print(g,p)

plt.plot(x,y)
ymax = max(y)
xmax = x[y.index(ymax)]
plt.annotate('Lag:'+str(xmax) + ', R:' + str(ymax), xy=(xmax, ymax))
plt.xlabel('Lag (seconds)')
plt.ylabel('Cross-correlation')
plt.figure()

LLR = pd.DataFrame(data={'x':x,'y':y})
LLR_ratio = np.nansum(LLR['y'].mask(LLR['x']>=0,np.nan).values) / np.nansum(LLR['y'].mask(LLR['x']<=0,np.nan).values)
print(LLR_ratio)