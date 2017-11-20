# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 11:53:24 2017

@author: Dieter Erben
"""

import pandas as pd, numpy as np

kld = pd.read_sas('/wrds/kld/sasdata/history.sas7bdat')
kld = kld[(kld.YEAR > 2005) & (kld.YEAR < 2017)]
kld  = kld.dropna(subset=['CUSIP'])


compustat = pd.read_stata('/scratch/nd/comp/funda.dta', convert_categoricals=False)
compustat = compustat[(compustat.fyear > 2005) & (compustat.fyear < 2017)]
compustat  = compustat.dropna(subset=['cusip'])

kld_cusips = kld.CUSIP
kld_cusips = kld_cusips.apply(lambda x: x.decode().rjust(9, '0')[:-1] if len(x)!=8 else x.decode())
compustat_cusip = compustat.cusip.str[:-1]
kld = kld.assign(CUSIP=kld_cusips)
compustat = compustat.assign(cusip=compustat_cusip)

#compustat2 = compustat.loc[(compustat['indfmt'] == 'INDL') & (compustat['datafmt'] == 'STD')] # length 123419
compustat2 = compustat.groupby(['cusip','fyear']) #length 124067
compustat2 = compustat2.first() # same length, gets first member of group
compustat2.reset_index(inplace=True)
comb = kld.merge(compustat2,left_on=['CUSIP','YEAR'],right_on=['cusip','fyear'])
comb.head()
'''
len(comb) is 22255
len(kld) is 30063
len(compustat) is 124067


count     218339
unique         2
top         INDL
freq      205006

count     218339
unique         2
top          STD
freq      136752



def get_first(grp):
    output = pd.DataFrame()
    sample = grp
    first = sample[0]
    output=output.append(result,ignore_index=True)
    return output

compustat4 = compustat3.apply(get_first)


t1 CUSIP YEAR
t2 cusip fyear

Length 7 examples
17765, 17778, 17780, 17783

17765    b'2567105'
17778    b'3654100'mer.
17780    b'2824100'
17783    b'4225108'

ABAX    002567105
ABMD    003654100
ABT     002824100
ACAD   004225108


Length 6 examples
17760, 17777, 17782

360206
957100

000360206
000957100

AAON
ACA



00846U10
00846U101

13817101
013872106

04543P10
04543P100

00949P10
00949P108

360206
000360206

98986T10
98986T108

98979J10
98979J109

98979G10
98979G105

98978V10
98978V103

98981710
989817101
'''