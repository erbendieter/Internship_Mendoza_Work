# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 10:58:35 2017

@author: Dieter Erben
"""
import pandas as pd, numpy as np
import statsmodels.api as sm

dsf = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsf.sas7bdat')
dsfhdr = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsfhdr.sas7bdat')

#permnos=dsfhdr[['PERMNO', 'HTICK']]
#permnos.PERMNO=permnos.PERMNO.astype(int)
# permnos.HTICK=[x.decode() for x in permnos.HTICK]
#permnos.columns=['PERMNO', 'Ticker']
#permnos.to_csv('permnos.csv',index=False)

returns=dsf[['PERMNO', 'DATE', 'RET']]
returns=returns.dropna()
returns.DATE = pd.to_timedelta(returns.DATE, unit='D') + pd.Timestamp('1960-1-1')
returns.PERMNO=returns.PERMNO.astype(int)

dsi = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsi.sas7bdat')
dsi.DATE = pd.to_timedelta(dsi.DATE.astype(int), unit='D') + pd.Timestamp('1960-1-1')
ewret=dsi[['DATE','ewretd']].dropna()

fama = pd.read_csv('F-F_Research_Data_Factors_daily.CSV', parse_dates=['DATE'])
momentum = pd.read_csv('F-F_Momentum_Factor_daily.CSV', parse_dates=['DATE'])
fama=pd.merge(fama, momentum, on='DATE')

dates = [pd.Timestamp('2000-07-21'),pd.Timestamp('2015-12-21'),pd.Timestamp('2017-01-24')]
groups = returns.groupby('PERMNO')

def abrets(grp):
    output = pd.DataFrame()
    sample = grp
    sample = pd.merge(sample, fama, on='DATE')
    sample = pd.merge(sample, ewret, on='DATE')
    sample['const']=1
    for x in dates:
        try:
            idx = sample.index[sample.DATE >= x][0]
        except IndexError:
            continue
        if idx<225 or len(sample)-idx<26: continue
        period51 = sample.loc[idx-25:idx+25]
        period25 = sample.loc[idx-12:idx+12]
        period05 = sample.loc[idx-2:idx+2]
        period03 = sample.loc[idx-1:idx+1]
        period200 = sample.loc[idx-225:idx-25]
        model_mkt = sm.OLS(period200.RET - period200.RF, period200[['Mkt-RF','const']]).fit()
        model_ff4 = sm.OLS(period200.RET - period200.RF, period200[['Mkt-RF','SMB','HML','Mom','const']]).fit()
        resid_mkt=period51.RET - period51.RF - model_mkt.predict(period51[['Mkt-RF','const']])
        resid_ff4=period51.RET - period51.RF - model_ff4.predict(period51[['Mkt-RF','SMB','HML','Mom','const']])
        result=pd.Series({'date':x})
        for winhalfsize in [25, 12, 2, 1]:
            car = np.prod(resid_mkt[25-winhalfsize:26+winhalfsize] +1)-1
            result=result.append(pd.Series({'car_ff1const_{:02}'.format(winhalfsize*2+1): car}))
            car = np.prod(resid_ff4[25-winhalfsize:26+winhalfsize] +1)-1
            result=result.append(pd.Series({'car_ff4const_{:02}'.format(winhalfsize*2+1): car}))
        output=output.append(result,ignore_index=True)
    return output


ssmp = returns[(returns['PERMNO'] == 10001) | (returns['PERMNO'] == 10002) | (returns['PERMNO'] == 10003) |(returns['PERMNO'] == 10004)]


results = returns.groupby('PERMNO').apply(abrets).dropna()

#res_perm=pd.merge(permnos, results, left_index=True, right_index=True)
results.reset_index(level=1,drop=True)[['date', 'car_ff1const_03', 'car_ff1const_05', 'car_ff1const_25', 'car_ff1const_51', 'car_ff4const_03', 'car_ff4const_05', 'car_ff4const_25', 'car_ff4const_51']].to_csv('car4.csv')