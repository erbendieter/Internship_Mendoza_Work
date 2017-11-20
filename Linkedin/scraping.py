import pandas as pd, numpy as np
os.chdir('c:\\Users\Dieter Erben\desktop\Mendoza Summer\Linkedin')

#Engagement Partner Last Name	Engagement Partner First Name	Engagement Partner Middle Name
#Firm Name
#First Space LAst
#First %20 Last

dfo = pd.read_csv('Unique Partners from PCAOB 070717.csv')

red = dfo[['Firm Name','Engagement Partner Last Name','Engagement Partner First Name',
'Engagement Partner Middle Name']]

dataframe["period"] = dataframe["Year"].map(str) + dataframe["quarter"]

df['CompleteName'] = df['Engagement Partner First Name'] + ' ' + df['Engagement Partner Last Name']
df['CompleteNameURL'] = df['Engagement Partner First Name'] + '%20' + df['Engagement Partner Last Name']

df.to_csv('LinkedinScraping.csv',index=False)