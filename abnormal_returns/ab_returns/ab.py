# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:01:07 2017

@author: Dieter Erben
"""

import pandas as pd, numpy as np
import statsmodels.api as sm

weighted_ret = pd.read_sas('dsi.sas7bdat')

weighted_ret.DATE = pd.to_timedelta(weighted_ret.DATE, unit='D') + pd.Timestamp('1960-1-1')
weighted_ret = weighted_ret[['DATE','vwretx']]

returns = pd.read_csv('abreturnspermco.csv',na_values=['B','C']).dropna()

companies = pd.read_csv('companies.csv')


#perm1 = companies[['permno1','Date_Announced']]
#perm1 = perm1.rename(index=str,columns={'permno1':'permno'})
#perm1 = perm1.dropna()
#perm2 = companies[['permno2','Date_Announced']]
#perm2 = perm2.rename(index=str,columns={'permno2':'permno'})
#perm2 = perm2.dropna()
#perm3 = companies[['permno3','Date_Announced']]
#perm3 = perm3.rename(index=str,columns={'permno3':'permno'})
#perm3 = perm3.dropna()

#perm = pd.concat([perm1,perm2,perm3])
perm = companies[['permco','Date_Announced']]
perm = perm.rename(columns={"Date_Announced": "date_announced"})
perm.date_announced = pd.to_datetime(perm.date_announced)

def abrets(row):
    permco = row.permco
    date_ann = row.date_announced
    sample = returns[returns.PERMCO==permco]
    sample=sample.assign(date=pd.to_datetime(sample.date,format='%Y%m%d'))
    sample = sample.rename(index=str,columns={'date':'DATE'})
    sample = pd.merge(sample,weighted_ret,how='left',on='DATE')
    
    try:
        ind = sample.index[sample.DATE >= date_ann][0]
    except IndexError:
        return pd.Series()

#Regression
#200 day period
    if ind<210: return pd.Series()
    
    period = sample.loc[ind-210:ind-11]
    x = period.RET
    x = sm.add_constant(x)
    y = period.vwretx
    model = sm.OLS(y, x).fit()
    period5 = sample.loc[ind-2:ind+2]
    period5['predict'] = model.predict(sm.add_constant(period5.RET))
    period5['residual'] = period5.RET-period5.predict
    period5['log'] = np.log(period5.residual+1)
    creturn = np.sum(period5.log)
    const = model.params.iloc[0]
    param1 = model.params.iloc[1]
    tvalue1 = model.tvalues.iloc[0]
    tvalue2 = model.tvalues.iloc[1]
    return pd.Series({'creturn':creturn, 'const':const,
                      'param1':param1, 'tvalue1':tvalue1,
                      'tvalue2':tvalue2})

result = perm.apply(abrets, axis=1)

mer = pd.merge(companies,result,left_index=True,right_index=True)

mer.to_csv('output.csv')
