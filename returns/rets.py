# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:53:05 2017

@author: Dieter Erben
"""

import pandas as pd, numpy as np
import statsmodels.api as sm

returns = pd.read_csv('return.csv', na_values="C").dropna()
returns.date = returns.date//100

fama = pd.read_csv('fama.csv')
momentum = pd.read_csv('mom.csv')

model = pd.merge(fama,momentum,how='inner',on='date')
both = pd.merge(returns,model,how='inner',on='date')

honda = both[both.PERMCO == 2172]
ford = both[both.PERMCO == 20750]
toyota = both[both.PERMCO == 4521]
gm1 = both[both.PERMCO == 20799]
gm2 = both[both.PERMCO == 53554]

companies = [honda,ford,toyota,gm1,gm2]

def syn(company):
    company['dep'] = company.RET - company.RF

    x = company[['SMB','HML','Mom','Mkt-RF']]
    y = company.dep
    model = sm.OLS(y, x).fit()
    model.summary()
    company['predict'] = model.predict(x)
    company['residual'] = company.RET - company.predict - company.RF

    company = company[['PERMNO','date','COMNAM','PERMCO',
              'RET','RF','predict','residual']]
    company['ret-rf'] = company.RET - company.RF
    company['residual+predict'] = company.residual + company.predict
    company['ret-expret'] = company.residual + company.RF
    company['1+(ret-exp)'] = 1 + company['ret-expret']
    company['CAR'] = np.log(company['1+(ret-exp)'])
    company['Ret'] = np.log(1+company['RET'])
    company = company[['PERMNO','date','COMNAM','PERMCO',
                       'CAR','Ret']]
    return company

final = [syn(x) for x in companies]

final = pd.concat(final)
final.to_csv('output.csv',index=False)

#sample = both[:10]
#sample['dep'] = sample.RET - sample.RF
#
#sample['ind1'] = sample.SMB
#sample['ind2'] = sample.HML
#sample['ind3'] = sample['Mom']
#
#sample2 = sample[['PERMNO','dep',
#                'ind1','ind2','ind3']]
#
#x = sample2[['ind1','ind2','ind3']]
#y = sample2.dep
