import pandas as pd, numpy as np, tldextract

from compsim.company_name_similarity import CompanyNameSimilarity
cm = CompanyNameSimilarity()

#cm.match_score

df1 = pd.read_csv("reviews_Nan_Li_1.csv",na_values='na')
df2 = pd.read_csv("reviews_Nan_Li_2.csv",na_values='na')
df = pd.concat([df1, df2], ignore_index=True)


gd = df[["FK_employerId","cityName","metroName","stateName","FK_countryId","name","shortName","websiteURL"]]

cb = pd.read_excel("crunchbase_firm_list.xlsx", dtype={'company_name':np.str},na_values='na')
cb['ID'] = cb.index

gd = gd.drop_duplicates(subset='FK_employerId')

def tld(x):
	if pd.isnull(x): return np.nan
	obj=tldextract.extract(x)
	return obj.domain+'.'+obj.suffix

gd=gd.assign(dom=[tld(x) for x in gd.websiteURL])
cb=cb.assign(dom=[tld(x) for x in cb.domain])

merboth = pd.merge(cb,gd,how='inner', on='dom')

ids = merboth.ID
cbu = cb[~cb['ID'].isin(ids)]
ids2 = merboth.FK_employerId
gdu = gd[~gd['FK_employerId'].isin(ids2)]

#[cm.match_score(x[1].company_name,x[1].shortName) for x in df.iterrows()]

def sco(x):
	scores = [np.nan if pd.isnull(x[1].shortName) else cm.match_score(x[1].company_name,x[1].shortName) for x in x.iterrows()]
	return x.iloc[np.argmax(scores)]

# Work with sample of 1000 company names
samp = merboth.iloc[1:1001]
sgru = samp.groupby(by='dom')
a = sgru.apply(sco)

# Full set
allg = merboth.groupby(by='dom')
alld = allg.apply(sco)





###################################################################

g = pd.DataFrame(['A','B','A','C','D','D','E'])

# Group by the contents of column 0 
gg = g.groupby(0)  

# Create a DataFrame with the counts of each letter
histo = gg.apply(lambda x: x.count())

for x in sgru:
	print(sgru.index())


for x in sgru.index():
	gr = sgru.get_group(samp.dom[x])
	sco(gr)

sgru.apply(func, *args, **kwargs)

[sgru.get_group(samp.dom[x]) for x in sgru.iterrows()]

sgru.get_group(samp.dom[1])
sco(sgru.get_group('actofit.com'))


for group in samp.groupby('dom'):
    sco(group)


def beb(x):
	grou = [x.get_group(samp.dom[x] for x in )]