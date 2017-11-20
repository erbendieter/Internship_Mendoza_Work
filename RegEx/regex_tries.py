# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:46:38 2017

@author: Dieter Erben
"""

import pandas as pd, re
df = pd.read_csv('fwdlooking.csv')
#df2 = df[:3143]
#streetsdf = pd.read_csv('streets.csv')
#streets = streetsdf.Street.tolist()

def reg(x):
    # Numbers and letters
    srep = re.sub(r'[A-Za-z]+\d+[A-Za-z-()]*|[A-Za-z]*\d+[A-Za-z(-]+[A-Za-z)\.]+',"",x,flags=re.IGNORECASE)
    # Dates
    srep = re.sub(r'\b[1][89][0-9][0-9]\b|\b[2][0][0-4][0-9]\b|\b\d{2}\/\d{2}\/\d{2}\b|\b\d{2}\/\d{2}\/\d{4}\b|\b\d{2}\-\d{2}\-\d{2}\b|\b\d{2}\-\d{2}\-\d{4}\b|\byear *\d{2}\b|\bfy *\d{2}\b|(jan(uary)*\.{0,1}|feb(ruary)*\.{0,1}|mar(ch)*\.{0,1}|apr(il)*\.{0,1}|may\.{0,1}|june*\.{0,1}|july*\.{0,1}|aug(ust)*\.{0,1}|sep(tember)*\.{0,1}|sept(ember)*\.{0,1}|oct(ober)*\.{0,1}|nov(ember)*\.{0,1}|dec(ember)*\.{0,1}).{1,10}',"",srep,flags=re.IGNORECASE)
    # Time
    srep = re.sub(r'\b\d{1,2}:\d{2}\b|\b\d{1,2}(-)*\d*( )*[ap]\.*[m]\.*\b',"",srep,flags=re.IGNORECASE)
    # Phone Numbers
    srep = re.sub(r'[[0-9]*[- .]?[\(]?\d{3}[\)]?[ ]?[-.]?\d{3}[-.]?\d{4}|[[0-9]?[- .]?\d{3}[-.]?\d{4}',"",srep,flags=re.IGNORECASE)
    # Zip Codes
    srep = re.sub(r'(AL|AK|AZ|AR|CA|CO|CT|DC|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montxana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming) *\d{5}(-\d{4})?',"",srep,flags=re.IGNORECASE)
    
    # Age exclusions
    srep = re.sub(r', \d{2},|age (of )?\d{2}|\d{2}[ -]?year[s-]?|turn[s]? \d{2}',"",srep,flags=re.IGNORECASE)
    # Other exclusions
    srep = re.sub(r'(no.|tiers?|sections?|districts?|pages?|pp?\.?|(sub)?chapters?|ch.) ?\d+[-.]*\d*|24[ -]hours?|\d+ words?',"",srep,flags=re.IGNORECASE)
    
    numbers = len(re.findall(r'\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    dollars = len(re.findall(r'\$ ?\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    return numbers, dollars








def regnum(x):
    # Numbers and letters
    srep = re.sub(r'[A-Za-z]+\d+[A-Za-z-()]*|[A-Za-z]*\d+[A-Za-z(-]+[A-Za-z)\.]+',"",x,flags=re.IGNORECASE)
    # Dates
    srep = re.sub(r'\b[1][89][0-9][0-9]\b|\b[2][0][0-4][0-9]\b|\b\d{2}\/\d{2}\/\d{2}\b|\b\d{2}\/\d{2}\/\d{4}\b|\b\d{2}\-\d{2}\-\d{2}\b|\b\d{2}\-\d{2}\-\d{4}\b|\byear *\d{2}\b|\bfy *\d{2}\b|(jan(uary)*\.{0,1}|feb(ruary)*\.{0,1}|mar(ch)*\.{0,1}|apr(il)*\.{0,1}|may\.{0,1}|june*\.{0,1}|july*\.{0,1}|aug(ust)*\.{0,1}|sep(tember)*\.{0,1}|sept(ember)*\.{0,1}|oct(ober)*\.{0,1}|nov(ember)*\.{0,1}|dec(ember)*\.{0,1}).{1,10}',"",srep,flags=re.IGNORECASE)
    # Time
    srep = re.sub(r'\b\d{1,2}:\d{2}\b|\b\d{1,2}(-)*\d*( )*[ap]\.*[m]\.*\b',"",srep,flags=re.IGNORECASE)
    # Phone Numbers
    srep = re.sub(r'[[0-9]*[- .]?[\(]?\d{3}[\)]?[ ]?[-.]?\d{3}[-.]?\d{4}|[[0-9]?[- .]?\d{3}[-.]?\d{4}',"",srep,flags=re.IGNORECASE)
    # Zip Codes
    srep = re.sub(r'(AL|AK|AZ|AR|CA|CO|CT|DC|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montxana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming) *\d{5}(-\d{4})?',"",srep,flags=re.IGNORECASE)
    
    # Age exclusions
    srep = re.sub(r', \d{2},|age (of )?\d{2}|\d{2}[ -]?year[s-]?|turn[s]? \d{2}',"",srep,flags=re.IGNORECASE)
    # Other exclusions
    srep = re.sub(r'(no.|tiers?|sections?|districts?|pages?|pp?\.?|(sub)?chapters?|ch.) ?\d+[-.]*\d*|24[ -]hours?|\d+ words?',"",srep,flags=re.IGNORECASE)
    
    numbers = len(re.findall(r'\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    return numbers

def regdol(x):
    # Numbers and letters
    srep = re.sub(r'[A-Za-z]+\d+[A-Za-z-()]*|[A-Za-z]*\d+[A-Za-z(-]+[A-Za-z)\.]+',"",x,flags=re.IGNORECASE)
    # Dates
    srep = re.sub(r'\b[1][89][0-9][0-9]\b|\b[2][0][0-4][0-9]\b|\b\d{2}\/\d{2}\/\d{2}\b|\b\d{2}\/\d{2}\/\d{4}\b|\b\d{2}\-\d{2}\-\d{2}\b|\b\d{2}\-\d{2}\-\d{4}\b|\byear *\d{2}\b|\bfy *\d{2}\b|(jan(uary)*\.{0,1}|feb(ruary)*\.{0,1}|mar(ch)*\.{0,1}|apr(il)*\.{0,1}|may\.{0,1}|june*\.{0,1}|july*\.{0,1}|aug(ust)*\.{0,1}|sep(tember)*\.{0,1}|sept(ember)*\.{0,1}|oct(ober)*\.{0,1}|nov(ember)*\.{0,1}|dec(ember)*\.{0,1}).{1,10}',"",srep,flags=re.IGNORECASE)
    # Time
    srep = re.sub(r'\b\d{1,2}:\d{2}\b|\b\d{1,2}(-)*\d*( )*[ap]\.*[m]\.*\b',"",srep,flags=re.IGNORECASE)
    # Phone Numbers
    srep = re.sub(r'[[0-9]*[- .]?[\(]?\d{3}[\)]?[ ]?[-.]?\d{3}[-.]?\d{4}|[[0-9]?[- .]?\d{3}[-.]?\d{4}',"",srep,flags=re.IGNORECASE)
    # Zip Codes
    srep = re.sub(r'(AL|AK|AZ|AR|CA|CO|CT|DC|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montxana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming) *\d{5}(-\d{4})?',"",srep,flags=re.IGNORECASE)
    
    # Age exclusions
    srep = re.sub(r', \d{2},|age (of )?\d{2}|\d{2}[ -]?year[s-]?|turn[s]? \d{2}',"",srep,flags=re.IGNORECASE)
    # Other exclusions
    srep = re.sub(r'(no.|tiers?|sections?|districts?|pages?|pp?\.?|(sub)?chapters?|ch.) ?\d+[-.]*\d*|24[ -]hours?|\d+ words?',"",srep,flags=re.IGNORECASE)
    
    dollars = len(re.findall(r'\$ ?\d+[.,]*\d*', srep, flags=re.IGNORECASE))
    return dollars

output = pd.DataFrame({'task1part1_number_count': df2.KEY_SENTENCES.apply(lambda x: x if pd.isnull(x) else regnum(x)),'task1part2_dollar_count': df2.KEY_SENTENCES.apply(lambda x: x if pd.isnull(x) else regdol(x))})

output = pd.DataFrame(df2.KEY_SENTENCES.apply(lambda x: x if pd.isnull(x) else reg(x)))
output = pd.DataFrame(output['KEY_SENTENCES'].values.tolist(), columns=['numbers','dollars'])

output.to_csv('out.csv')

    #Addresses
    #Exclude all numbers in the 30 characters preceding street, avenue, road, boulevard, plaza, etc. (including common abbreviations like st and ave). Is there a comprehensive list of common street terms and abbreviations available?
    #srep = re.sub(r'(.){1,30}\b((ALLEE)|(ALLEY)|(ALLY)|(ALY)|(ANEX)|(ANNEX)|(ANNX)|(ANX)|(ARC)|(ARCADE)|(AV)|(AVE)|(AVEN)|(AVENU)|(AVENUE)|(AVN)|(AVNUE)|(BAYOO)|(BAYOU)|(BCH)|(BEACH)|(BEND)|(BG)|(BGS)|(BLF)|(BLFS)|(BLUF)|(BLUFF)|(BLUFFS)|(BLVD)|(BND)|(BOT)|(BOTTM)|(BOTTOM)|(BOUL)|(BOULEVARD)|(BOULV)|(BR)|(BRANCH)|(BRDGE)|(BRG)|(BRIDGE)|(BRK)|(BRKS)|(BRNCH)|(BROOK)|(BROOKS)|(BTM)|(BURG)|(BURGS)|(BYP)|(BYPA)|(BYPAS)|(BYPASS)|(BYPS)|(BYU)|(CAMP)|(CANYN)|(CANYON)|(CAPE)|(CAUSEWAY)|(CAUSWA)|(CEN)|(CENT)|(CENTER)|(CENTERS)|(CENTR)|(CENTRE)|(CIR)|(CIRC)|(CIRCL)|(CIRCLE)|(CIRCLES)|(CIRS)|(CLB)|(CLF)|(CLFS)|(CLIFF)|(CLIFFS)|(CLUB)|(CMN)|(CMNS)|(CMP)|(CNTER)|(CNTR)|(CNYN)|(COMMON)|(COMMONS)|(COR)|(CORNER)|(CORNERS)|(CORS)|(COURSE)|(COURT)|(COURTS)|(COVE)|(COVES)|(CP)|(CPE)|(CRCL)|(CRCLE)|(CREEK)|(CRES)|(CRESCENT)|(CREST)|(CRK)|(CROSSING)|(CROSSROAD)|(CROSSROADS)|(CRSE)|(CRSENT)|(CRSNT)|(CRSSNG)|(CRST)|(CSWY)|(CT)|(CTR)|(CTRS)|(CTS)|(CURV)|(CURVE)|(CV)|(CVS)|(CYN)|(DALE)|(DAM)|(DIV)|(DIVIDE)|(DL)|(DM)|(DR)|(DRIV)|(DRIVE)|(DRIVES)|(DRS)|(DRV)|(DV)|(DVD)|(EST)|(ESTATE)|(ESTATES)|(ESTS)|(EXP)|(EXPR)|(EXPRESS)|(EXPRESSWAY)|(EXPW)|(EXPY)|(EXT)|(EXTENSION)|(EXTENSIONS)|(EXTN)|(EXTNSN)|(EXTS)|(FALL)|(FALLS)|(FERRY)|(FIELD)|(FIELDS)|(FLAT)|(FLATS)|(FLD)|(FLDS)|(FLS)|(FLT)|(FLTS)|(FORD)|(FORDS)|(FOREST)|(FORESTS)|(FORG)|(FORGE)|(FORGES)|(FORK)|(FORKS)|(FORT)|(FRD)|(FRDS)|(FREEWAY)|(FREEWY)|(FRG)|(FRGS)|(FRK)|(FRKS)|(FRRY)|(FRST)|(FRT)|(FRWAY)|(FRWY)|(FRY)|(FT)|(FWY)|(GARDEN)|(GARDENS)|(GARDN)|(GATEWAY)|(GATEWY)|(GATWAY)|(GDN)|(GDNS)|(GLEN)|(GLENS)|(GLN)|(GLNS)|(GRDEN)|(GRDN)|(GRDNS)|(GREEN)|(GREENS)|(GRN)|(GRNS)|(GROV)|(GROVE)|(GROVES)|(GRV)|(GRVS)|(GTWAY)|(GTWY)|(HARB)|(HARBOR)|(HARBORS)|(HARBR)|(HAVEN)|(HBR)|(HBRS)|(HEIGHTS)|(HIGHWAY)|(HIGHWY)|(HILL)|(HILLS)|(HIWAY)|(HIWY)|(HL)|(HLLW)|(HLS)|(HOLLOW)|(HOLLOWS)|(HOLW)|(HOLWS)|(HRBOR)|(HT)|(HTS)|(HVN)|(HWAY)|(HWY)|(INLET)|(INLT)|(ISLAND)|(ISLANDS)|(ISLE)|(ISLES)|(ISLND)|(ISLNDS)|(ISS)|(JCT)|(JCTION)|(JCTN)|(JCTNS)|(JCTS)|(JUNCTION)|(JUNCTIONS)|(JUNCTN)|(JUNCTON)|(KEY)|(KEYS)|(KNL)|(KNLS)|(KNOL)|(KNOLL)|(KNOLLS)|(KY)|(KYS)|(LAKE)|(LAKES)|(LAND)|(LANDING)|(LANE)|(LCK)|(LCKS)|(LDG)|(LDGE)|(LF)|(LGT)|(LGTS)|(LIGHT)|(LIGHTS)|(LK)|(LKS)|(LN)|(LNDG)|(LNDNG)|(LOAF)|(LOCK)|(LOCKS)|(LODG)|(LODGE)|(LOOP)|(LOOPS)|(MALL)|(MANOR)|(MANORS)|(MDW)|(MDWS)|(MEADOW)|(MEADOWS)|(MEDOWS)|(MEWS)|(MILL)|(MILLS)|(MISSION)|(MISSN)|(ML)|(MLS)|(MNR)|(MNRS)|(MNT)|(MNTAIN)|(MNTN)|(MNTNS)|(MOTORWAY)|(MOUNT)|(MOUNTAIN)|(MOUNTAINS)|(MOUNTIN)|(MSN)|(MSSN)|(MT)|(MTIN)|(MTN)|(MTNS)|(MTWY)|(NCK)|(NECK)|(OPAS)|(ORCH)|(ORCHARD)|(ORCHRD)|(OVAL)|(OVERPASS)|(OVL)|(PARK)|(PARKS)|(PARKWAY)|(PARKWAYS)|(PARKWY)|(PASS)|(PASSAGE)|(PATH)|(PATHS)|(PIKE)|(PIKES)|(PINE)|(PINES)|(PKWAY)|(PKWY)|(PKWYS)|(PKY)|(PL)|(PLACE)|(PLAIN)|(PLAINS)|(PLAZA)|(PLN)|(PLNS)|(PLZ)|(PLZA)|(PNE)|(PNES)|(POINT)|(POINTS)|(PORT)|(PORTS)|(PR)|(PRAIRIE)|(PRK)|(PRR)|(PRT)|(PRTS)|(PSGE)|(PT)|(PTS)|(RAD)|(RADIAL)|(RADIEL)|(RADL)|(RAMP)|(RANCH)|(RANCHES)|(RAPID)|(RAPIDS)|(RD)|(RDG)|(RDGE)|(RDGS)|(RDS)|(REST)|(RIDGE)|(RIDGES)|(RIV)|(RIVER)|(RIVR)|(RNCH)|(RNCHS)|(ROAD)|(ROADS)|(ROUTE)|(ROW)|(RPD)|(RPDS)|(RST)|(RTE)|(RUE)|(RUN)|(RVR)|(SHL)|(SHLS)|(SHOAL)|(SHOALS)|(SHOAR)|(SHOARS)|(SHORE)|(SHORES)|(SHR)|(SHRS)|(SKWY)|(SKYWAY)|(SMT)|(SPG)|(SPGS)|(SPNG)|(SPNGS)|(SPRING)|(SPRINGS)|(SPRNG)|(SPRNGS)|(SPUR)|(SPURS)|(SQ)|(SQR)|(SQRE)|(SQRS)|(SQS)|(SQU)|(SQUARE)|(SQUARES)|(ST)|(STA)|(STATION)|(STATN)|(STN)|(STR)|(STRA)|(STRAV)|(STRAVEN)|(STRAVENUE)|(STRAVN)|(STREAM)|(STREET)|(STREETS)|(STREME)|(STRM)|(STRT)|(STRVN)|(STRVNUE)|(STS)|(SUMIT)|(SUMITT)|(SUMMIT)|(TER)|(TERR)|(TERRACE)|(THROUGHWAY)|(TPKE)|(TRACE)|(TRACES)|(TRACK)|(TRACKS)|(TRAFFICWAY)|(TRAIL)|(TRAILER)|(TRAILS)|(TRAK)|(TRCE)|(TRFY)|(TRK)|(TRKS)|(TRL)|(TRLR)|(TRLRS)|(TRLS)|(TRNPK)|(TRWY)|(TUNEL)|(TUNL)|(TUNLS)|(TUNNEL)|(TUNNELS)|(TUNNL)|(TURNPIKE)|(TURNPK)|(UN)|(UNDERPASS)|(UNION)|(UNIONS)|(UNS)|(UPAS)|(VALLEY)|(VALLEYS)|(VALLY)|(VDCT)|(VIA)|(VIADCT)|(VIADUCT)|(VIEW)|(VIEWS)|(VILL)|(VILLAG)|(VILLAGE)|(VILLAGES)|(VILLE)|(VILLG)|(VILLIAGE)|(VIS)|(VIST)|(VISTA)|(VL)|(VLG)|(VLGS)|(VLLY)|(VLY)|(VLYS)|(VST)|(VSTA)|(VW)|(VWS)|(WALK)|(WALKS)|(WALL)|(WAY)|(WAYS)|(WELL)|(WELLS)|(WL)|(WLS)|(WY)|(XING)|(XRD)|(XRDS))\b',"+++",srep,flags=re.IGNORECASE)