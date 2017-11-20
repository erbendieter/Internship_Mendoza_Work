import pandas as pd, numpy as np, os
import scipy
import statsmodels.api as sm
os.chdir('c:\\Users\Dieter Erben\desktop\Mendoza Summer')

def only_numbers(seq):
    return filter(type(seq).isdigit, seq)

ret = pd.read_csv('return.csv', na_values="C").dropna()
ret.date = ret.date//100

fama = pd.read_csv('fama.csv')
mom = pd.read_csv('mom.csv')

model = pd.merge(fama,mom,how='inner',on='date')
both = pd.merge(ret,model,how='inner',on='date')

honda = both[both.PERMCO == 2172]
ford = both[both.PERMCO == 20750]
toyota = both[both.PERMCO == 4521]
gm1 = both[both.PERMCO == 20799]
gm2 = both[both.PERMCO == 53554]

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

ford['dep'] = ford.RET - ford.RF

x = ford[['SMB','HML','Mom','Mkt-RF']]
y = ford.dep
model = sm.OLS(y, x).fit()
model.summary()
ford['predict'] = model.predict(x)
ford['residual'] = ford.RET - ford.predict - ford.RF

ford = ford[['PERMNO','date','COMNAM','PERMCO',
              'RET','RF','predict','residual']]
ford['ret-rf'] = ford.RET - ford.RF
ford['residual+predict'] = ford.residual + ford.predict
ford['ret-expret'] = ford.residual + ford.RF
ford['1+(ret-exp)'] = 1 + ford['ret-expret']
ford['CAR'] = np.log(ford['1+(ret-exp)'])
ford['Ret'] = np.log(1+ford['RET'])
finalford = ford[['PERMNO','date','COMNAM','PERMCO',
                   'CAR','Ret']]