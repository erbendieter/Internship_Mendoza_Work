import pandas as pd, numpy as np
import statsmodels.api as sm

companies = pd.read_csv('mgmt_declass_prop_8_17_2017.csv', parse_dates=['MeetingDate'], encoding='latin-1')
com_permco=companies[['MeetingDate', 'lpermco']].dropna().reset_index()
com_permno=companies[pd.isnull(companies.lpermco)][['MeetingDate', 'lpermno']].dropna().reset_index()
com_ticker=companies[pd.isnull(companies.lpermco)&pd.isnull(companies.lpermno)][['MeetingDate', 'Ticker']].dropna().reset_index()
com_ticker.Ticker=[ticker.encode() for ticker in com_ticker.Ticker]

permno1=com_permco.merge(dsfhdr[['PERMCO', 'PERMNO']], left_on='lpermco', right_on='PERMCO')
permno2=com_permno.merge(dsfhdr[['PERMNO']], left_on='lpermno', right_on='PERMNO')
permno3=com_ticker.merge(dsfhdr[['HTICK', 'PERMNO']], left_on='Ticker', right_on='HTICK')
permnos=pd.concat([permno1[['index', 'MeetingDate', 'PERMNO']], permno2[['index', 'MeetingDate', 'PERMNO']], permno3[['index', 'MeetingDate', 'PERMNO']]])
permnos.PERMNO=permnos.PERMNO.astype(int)
permnos=permnos.reset_index(drop=True)
permnos.to_csv('permnos.csv', index=False)

tickers=companies.Ticker
tickersb=[ticker.encode() for ticker in tickers]

""" #Run only once
dsf = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsf.sas7bdat')
dsfhdr = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsfhdr.sas7bdat')
permnos=dsfhdr[dsfhdr.HTICK.isin(tickersb)][['PERMNO', 'HTICK']]
permnos.PERMNO=permnos.PERMNO.astype(int)
permnos.HTICK=[x.decode() for x in permnos.HTICK]
permnos.columns=['PERMNO', 'Ticker']
permnos.to_csv('permnos.csv',index=False)

returns=dsf[dsf.PERMNO.isin(permnos.PERMNO)][['PERMNO', 'DATE', 'RET']]
returns=returns.dropna()
returns.DATE = pd.to_timedelta(returns.DATE, unit='D') + pd.Timestamp('1960-1-1')
returns.PERMNO=returns.PERMNO.astype(int)
returns.to_csv('returns.csv',index=False)
"""

#Import CRSP stock returns
returns = pd.read_csv('returns.csv', parse_dates=['DATE'])
permnos = pd.read_csv('permnos.csv')

#Import CRSP index file (dsi) as ewret (equal weighted market index)
dsi = pd.read_sas('/wrds/crsp/sasdata/a_stock/dsi.sas7bdat')
dsi.DATE = pd.to_timedelta(dsi.DATE.astype(int), unit='D') + pd.Timestamp('1960-1-1')
ewret=dsi[['DATE','ewretd']].dropna()

fama = pd.read_csv('F-F_Research_Data_Factors_daily.CSV', parse_dates=['DATE'])
momentum = pd.read_csv('F-F_Momentum_Factor_daily.CSV', parse_dates=['DATE'])
fama=pd.merge(fama, momentum, on='DATE')

#Main function to calculate abnormal returns based on each [PERMNO, Date_Announced] pair
def abrets(row):
    sample = returns[returns.PERMNO==row.PERMNO]
    sample = pd.merge(sample, fama, on='DATE')
    sample = pd.merge(sample, ewret, on='DATE')
    sample['const']=1
    try:
        idx = sample.index[sample.DATE >= row.MeetingDate][0]
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

#Apply main function and output results
#perm=permnos.merge(companies, on='Ticker')
results = permnos.apply(abrets, axis=1).dropna()
res_perm=pd.merge(permnos, results, left_index=True, right_index=True)
res_perm.to_csv('car3.csv', index=False)
