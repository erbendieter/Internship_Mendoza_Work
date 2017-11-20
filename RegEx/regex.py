# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:38:43 2017

@author: Dieter Erben
"""
import pandas as pd, re
df = pd.read_csv('fwdlooking.csv')

# Dates
    pattern_dates = re.compile(r'\b[1][89][0-9][0-9]\b|\b[2][0][0-4][0-9]\b|\b\d{2}\/\d{2}\/\d{2}\b|\b\d{2}\/\d{2}\/\d{4}\b|\b\d{2}\-\d{2}\-\d{2}\b|\b\d{2}\-\d{2}\-\d{4}\b|\byear *\d{2}\b|\bfy *\d{2}\b|\b(jan(?:uary)?\.?|feb(?:ruary)?\.?|mar(?:ch)?\.?|apr(?:il)?\.?|may\.?|june?\.?|july?\.?|aug(?:ust)?\.?|sep(?:t?ember)?\.?|oct(?:ober)?\.?|nov(?:ember)?\.?|dec(?:ember)?\.?).{1,10}')
    # Time
    pattern_times = re.compile(r'\b\d{1,2}[:\-]\d{2}\b|\b(?:\d{1,2}[:\-]\d{1,2}|\d{1,2}) *[ap]\.?m?\.?\b')
    # Phone Numbers
    pattern_phones = re.compile(r'[[0-9]*[- .]?[\(]?\d{3}[\)]?[ ]?[-.]?\d{3}[-.]?\d{4}|[[0-9]?[- .]?\d{3}[-.]?\d{4}')
     # Zip Codes
    pattern_zip = re.compile(r'(AL|AK|AZ|AR|CA|CO|CT|DC|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming) *\d{5}(?:-\d{4})?')
    # Age exclusions
    pattern_age = re.compile(r', \d{2},|age (of )?\d{2}|\d{2}[ -]?year[s-]?|turn[s]? \d{2}')
    # Other exclusions
    pattern_other = re.compile(r'\b(?:no.|tier[a-z]*|[a-z]*section[a-z]*|[a-z]*district[a-z]*|page[a-z]*|pp?\.?|(?:sub)?chapter[a-z]*|ch.) *\d+[-\.]*\d*|24[ -]hour[a-z]*|\d+ words?')

def reg(x):
    #pattern_dollars = re.compile(r'\$\s*[\d\.,\-]+\b')
    #
    #numbers=pattern_numbers.findall(x)
    #dollars=pattern_dollars.findall(x)
    
    # Numbers and letters
    #srep = re.sub(r'[A-Za-z]+\d+[A-Za-z-()]*|[A-Za-z]*\d+[A-Za-z(-]+[A-Za-z)\.]+',"",x)
    
    srep = pattern_dates.sub("",x)
    srep = pattern_times.sub("",srep)
    srep = pattern_phones.sub("",srep)
    srep = pattern_zip.sub("",srep)
    srep = pattern_age.sub("",srep)
    srep = pattern_other.sub("",srep)
    
    numbers = len(re.findall(r'\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    dollars = len(re.findall(r'\$ ?\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    return numbers, dollars

output = pd.DataFrame(df.KEY_SENTENCES.apply(lambda x: x if pd.isnull(x) else reg(x)))
output = output['KEY_SENTENCES'].apply(pd.Series)
#output
output = output.rename(index=str, columns={0: "numbers", 1: "dollars"})

output.to_csv('out.csv')