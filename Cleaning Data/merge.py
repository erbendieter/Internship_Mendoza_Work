import pandas as pd, numpy as np, tldextract
from compsim.company_name_similarity import CompanyNameSimilarity
cm = CompanyNameSimilarity()


df1 = pd.read_csv("reviews_Nan_Li_1.csv",na_values='na')
df2 = pd.read_csv("reviews_Nan_Li_2.csv",na_values='na')
df = pd.concat([df1, df2], ignore_index=True)


gd = df[["FK_employerId","cityName","metroName","stateName","FK_countryId","name","shortName","websiteURL"]]

cb = pd.read_excel("crunchbase_firm_list.xlsx", dtype={'company_name':np.str},na_values='na')
cb['ID'] = cb.index

gd = gd.drop_duplicates(subset='FK_employerId')
gd.websiteURL = gd.websiteURL.str.replace('\.{2,}', '.')
cb.domain = cb.domain.str.replace('\.{2,}','.')

def tld(x):
	if pd.isnull(x): return np.nan
	obj=tldextract.extract(x)
	return obj.domain+'.'+obj.suffix

gd=gd.assign(dom=[tld(x) for x in gd.websiteURL])
cb=cb.assign(dom=[tld(x) for x in cb.domain])

merboth = pd.merge(cb,gd,how='inner', on='dom')

def sco(x):
	scores = [np.nan if pd.isnull(x[1].shortName) else cm.match_score(x[1].company_name,x[1].shortName) for x in x.iterrows()]
	return x.iloc[np.argmax(scores)]

# First trial with sample of 1000 company names
# samp = merboth.iloc[1:1001]
# sgru = samp.groupby(by='dom')
# a = sgru.apply(sco)

# Full set
allg = merboth.groupby(by='dom')
alld = allg.apply(sco)