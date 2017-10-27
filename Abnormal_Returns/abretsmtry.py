# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:46:29 2017

@author: Dieter Erben
"""

row = groups.get_group(93436)

def abrets(row):
    for x in dates:
        sample = row
        sample = pd.merge(sample, fama, on='DATE')
        sample = pd.merge(sample, ewret, on='DATE')
        sample['const']=1
        try:
            idx = sample.index[sample.DATE >= x][0]
        except IndexError:
            return pd.Series()
        if idx<225 or len(sample)-idx<26: return pd.Series()
        period51 = sample.loc[idx-25:idx+25]
        period25 = sample.loc[idx-12:idx+12]
        period05 = sample.loc[idx-2:idx+2]
        period03 = sample.loc[idx-1:idx+1]
        period200 = sample.loc[idx-225:idx-25]
        model_mkt = sm.OLS(period200.RET - period200.RF, period200[['Mkt-RF','const']]).fit()
        model_ff4 = sm.OLS(period200.RET - period200.RF, period200[['Mkt-RF','SMB','HML','Mom','const']]).fit()
        resid_mkt=period51.RET - period51.RF - model_mkt.predict(period51[['Mkt-RF','const']])
        resid_ff4=period51.RET - period51.RF - model_ff4.predict(period51[['Mkt-RF','SMB','HML','Mom','const']])
        result=pd.Series()
        for winhalfsize in [25, 12, 2, 1]:
            car = np.prod(resid_mkt[25-winhalfsize:26+winhalfsize] +1)-1
            result=result.append(pd.Series({'car_ff1const_{:02}'.format(winhalfsize*2+1): car}))
            car = np.prod(resid_ff4[25-winhalfsize:26+winhalfsize] +1)-1
            result=result.append(pd.Series({'car_ff4const_{:02}'.format(winhalfsize*2+1): car}))
        return result