############################
### Import, Clean, Merge ###
############################

library(dplyr); library(tidyr)

clientRoster = read.csv("valueFuzzyMerge/data/original/clientRoster.csv")

compustatSheet = read.csv("valueFuzzyMerge/data/original/compustatSheet.csv")


### Let's do some string tidying

# AT&T is a bit of an odd duck -- at one time it was AT&T Corp, but it is now
# AT&T Inc. Let's drop the AT&T Corp rows from the compustat data.

compustatSheet = compustatSheet[-(grep("AT&T CORP", compustatSheet$CONAME)),]

# Let's convert everything to lower case

clientRoster$cleanName = tolower(clientRoster$Company)

compustatSheet$CONAME = tolower(compustatSheet$CONAME)

# Now, let's get rid of some junk (e.g., co, corp, inc). These really do not
# help when it comes time to join these things.

clientRoster$cleanName = gsub("\\.|,","",clientRoster$cleanName)
clientRoster$cleanName = gsub(" inc$| corp$| co$| ltd$| -cl .$| cos$| companies$| company$| co inc$| plc$",
                              "", clientRoster$cleanName)
clientRoster$cleanName = gsub(" corporation$| incorporated$",
                              "", clientRoster$cleanName)

compustatSheet$CONAME = gsub(" inc$| corp$| co$| ltd$| -cl .$| cos$| companies$| company$| co inc$| plc$",
                              " ", compustatSheet$CONAME)

clientRoster$cleanName = stringr::str_trim(clientRoster$cleanName)

compustatSheet$CONAME = stringr::str_trim(compustatSheet$CONAME)

# We are going to run the same two lines again, just to get any stragglers:

clientRoster$cleanName = gsub("\\.|,","",clientRoster$cleanName)
clientRoster$cleanName = gsub(" inc$| corp$| co$| ltd$| -cl .$| cos$| companies$| company$| co inc$| plc$",
                              "", clientRoster$cleanName)
clientRoster$cleanName = gsub(" corporation$",
                              "", clientRoster$cleanName)

compustatSheet$CONAME = gsub(" inc$| corp$| co$| ltd$| -cl .$| cos$| companies$| company$| co inc$| plc$",
                                   " ", compustatSheet$CONAME)

# We also need to get rid of some puncutation; we could do it all in 1 swoop,
# but breaking it up is good for seeing what we did.

compustatSheet$CONAME = gsub("-", " ", compustatSheet$CONAME, perl = TRUE)

clientRoster$cleanName = gsub("-", " ", clientRoster$cleanName, perl = TRUE)

compustatSheet$CONAME = gsub(",", "", compustatSheet$CONAME, perl = TRUE)

clientRoster$cleanName = gsub(",", "", clientRoster$cleanName, perl = TRUE)

compustatSheet$CONAME = gsub("&", "", compustatSheet$CONAME, perl = TRUE)

clientRoster$cleanName = gsub("&", "", clientRoster$cleanName, perl = TRUE)

clientRoster$cleanName = gsub("^the ", "", clientRoster$cleanName, perl = TRUE)

# Recoding Time!

clientRoster$cleanName[grep("^3m .*", clientRoster$cleanName)] = "3m"

clientRoster$cleanName[grep("^20th century fox .*", clientRoster$cleanName)] = "20th century fox"

clientRoster$cleanName[grep("apple computer.", clientRoster$cleanName)] = "apple"

clientRoster$cleanName[grep("^att communications|^att international|^att technologies",
                            clientRoster$cleanName)] = "att"

clientRoster$cleanName[grep("^bristol m.*", clientRoster$cleanName)] = "bristol myers squibb"

clientRoster$cleanName[grep("^citib.*|citic.*", clientRoster$cleanName)] = "citigroup"

clientRoster$cleanName[grep("^dow chemical .*", clientRoster$cleanName)] = "dow chemical"

clientRoster$cleanName[grep("^dow jones", clientRoster$cleanName)] = "dow jones"

clientRoster$cleanName[grep("^du pont de nemours ei ", clientRoster$cleanName)] = "du pont de nemours"

compustatSheet$CONAME[grep("^du pont .*", compustatSheet$CONAME)] = "du pont de nemours"

clientRoster$cleanName[grep("^eli lilly", clientRoster$cleanName)] = "lilly (eli)"

clientRoster$cleanName[grep("^fisher price", clientRoster$cleanName)] = "fisher price"

clientRoster$cleanName[grep("^ford motor", clientRoster$cleanName)] = "ford motor"

clientRoster$cleanName[grep("^harley davidson", clientRoster$cleanName)] = "harley davidson"

clientRoster$cleanName[grep("^heinz", clientRoster$cleanName)] = "kraft heinz"

clientRoster$cleanName[grep("^hershey", clientRoster$cleanName)] = "hershey"

clientRoster$cleanName[grep("^hillshire farm$", clientRoster$cleanName)] = "hillshire brands"

clientRoster$cleanName[grep("^hj heinz", clientRoster$cleanName)] = "kraft heinz"

clientRoster$cleanName[grep("^honeywell", clientRoster$cleanName)] = "honeywell international"

clientRoster$cleanName[grep("^johnson johnson", clientRoster$cleanName)] = "johnson johnson"

clientRoster$cleanName[grep("^kraft$|^kraft food.*|^kraft general.*|^kraft refrig.*",
                            clientRoster$cleanName)] = "kraft heinz"

clientRoster$cleanName[grep("^mcdonald_s.*|^mcdonalds*|^mcdonalds restaurants", clientRoster$cleanName)] = "mcdonald's"

clientRoster$cleanName[grep("^morgan jp", clientRoster$cleanName)] = "morgan (j p)"

clientRoster$cleanName[grep("^nabisco", clientRoster$cleanName)] = "nabisco group holdings"

clientRoster$cleanName[grep("parker hannifan", clientRoster$cleanName)] = "parker hannifin"

clientRoster$cleanName[grep("pepsi cola|pepsico|pepsico international", clientRoster$cleanName)] = "pepsico"

clientRoster$cleanName[grep("^pfizer", clientRoster$cleanName)] = "pfizer"

clientRoster$cleanName[grep("^procter", clientRoster$cleanName)] = "procter gamble"

clientRoster$cleanName[grep("^reebok", clientRoster$cleanName)] = "reebok international"

clientRoster$cleanName[grep("^scholastic", clientRoster$cleanName)] = "scholastic"

clientRoster$cleanName[grep("^schwab charles", clientRoster$cleanName)] = "schwab (charles)"

clientRoster$cleanName[grep("^t rowe price", clientRoster$cleanName)] = "price (t. rowe) group"

clientRoster$cleanName[grep("^target stores", clientRoster$cleanName)] = "target"

clientRoster$cleanName[grep("texas insturments", clientRoster$cleanName)] = "texas instruments"

clientRoster$cleanName[grep("the coca cola company", clientRoster$cleanName)] = "coca cola"

clientRoster$cleanName[grep("the gillette company", clientRoster$cleanName)] = "gillette"

clientRoster$cleanName[grep("^time warner", clientRoster$cleanName)] = "time warner"

clientRoster$cleanName[grep("^ag edwards", clientRoster$cleanName)] = "edwards (a g)"

clientRoster$cleanName[grep("allstate insurance", clientRoster$cleanName)] = "allstate"

clientRoster$cleanName[grep("^bank of america|bankamerica", clientRoster$cleanName)] = "bank of america"

clientRoster$cleanName[grep("bank of boston", clientRoster$cleanName)] = "bankboston"

clientRoster$cleanName[grep("barnes noble bookstores", clientRoster$cleanName)] = "barnes  noble"

clientRoster$cleanName[grep("allergan hydron", clientRoster$cleanName)] = "allergan"

clientRoster$cleanName[grep("american express publishing",
                            clientRoster$cleanName)] = "american express"

clientRoster$cleanName[grep("avis rent a car system",
                            clientRoster$cleanName)] = "avis budget group"

clientRoster$cleanName[grep("bank of new york",
                            clientRoster$cleanName)] = "bank of new york mellon"

compustatSheet$CONAME[grep("c h robinson worldwide", compustatSheet$CONAME)] = "ch robinson worldwide"
compustatSheet$CONAME[grep("bard (c.r.)", compustatSheet$CONAME)] = "cr bard"
compustatSheet$CONAME[grep("dell technologies", compustatSheet$CONAME)] = "dell"
compustatSheet$CONAME[grep("lauder (estee)", compustatSheet$CONAME)] = "estee lauder"
clientRoster$cleanName[grep("guess'",clientRoster$cleanName)] = "guess"
compustatSheet$CONAME[grep("intl business machines", compustatSheet$CONAME)] = "international business machines"
compustatSheet$CONAME[grep("smucker (jm)", compustatSheet$CONAME)] = "j m smucker"
compustatSheet$CONAME[grep("paypal holdings", compustatSheet$CONAME)] = "paypal"
compustatSheet$CONAME[grep("disney (walt)", compustatSheet$CONAME)] = "walt disney"

# Let's make sure we do not have any trailing spaces.

clientRoster$cleanName = stringr::str_trim(clientRoster$cleanName)

compustatSheet$CONAME = stringr::str_trim(compustatSheet$CONAME)


### Selecting and Reshaping

compustatSheet = compustatSheet %>%
  select(X, CONAME, CUSIP) %>%
  unique()

compustatSheet = compustatSheet[!duplicated(compustatSheet$CONAME), ]


library(fuzzyjoin)

test2 = stringdist_left_join(clientRoster, compustatSheet, by = c("cleanName" = "CONAME"),
                     max_dist = .0250, method = "jw", p = .1, distance_col = "stringDistance")

write.csv(test, file = "valueFuzzyMerge/data/joinedData.csv")
