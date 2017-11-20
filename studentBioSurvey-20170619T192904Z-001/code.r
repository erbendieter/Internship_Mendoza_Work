

Some packages to install

install.packages(c("dplyr","httr","rvest",'rjson'))
library(dplyr); library(httr); library(rvest); library(rjson)

#lapply for loops.

#try catch example
lapply(1:length(allAPILinks), function(x) {
  tryCatch({
    Sys.sleep(2)
    fileName = paste("data/jsonRawRestaurants/", "file", x, ".json", sep = "")
    download.file(allAPILinks[[x]][1], destfile = fileName, method = "auto")
  },error = function(e){
    print(paste("no good:", x, sep = " "))
  })
})

#squasher and subsmash for combining files


debugonce(squasher)
#to show function step by step

#filtering and selecting
allReviewsDFR = allReviewsDFR %>% 
  filter(numberOfRatings > 0) %>% 
  select(id, name, industry, numberOfRatings, 
         ends_with("Rating")) %>% 
  filter(industry == 'Casual Restaurants'| industry == 'Upscale Restaurants'|industry == 'Fast-Food & Quick-Service Restaurants') %>% 
  mutate(Search='Restaurants')

#combining files
allReviewsCombined = rbind(allReviewsDFA, allReviewsDFH, allReviewsDFR)

#running a program with many cores, parallel
library(snow)
clnum = parallel::detectCores() - 1	#always leave one core open


cl = makeSOCKcluster(clnum)

#Have to load the packages again here.
clusterEvalQ(cl,library(dplyr))
clusterEvalQ(cl,library(rvest))
t1 = proc.time()
ldf = parLapply(cl, allReviewsCombined, companyScraper)
proc.time() - t1
stopCluster(cl)

#grepl looks for string and if false, meaning it does not show no good, it keeps it.
allReviews = allReviews[grepl("no good",allReviews)==FALSE]
allReviews = data.table::rbindlist(allReviews)


#add a new column with all text combined and add id number
allReviews = allReviews %>% 
  mutate(allText = paste(pros, cons, advice, sep = " "), 
         id = 1:nrow(allReviews)) #%>%

#getting rid of entries in other languages
germans = grep("(\\b[Dd]er\\b)|(\\bund\\b)|(\\bist\\b)|(\\bsehr\\b)|(\\b[Gg]ute\\b)|(\\b[Nn]ach\\b)|ä|ö|ü|ß", allReviews$allText)

spanish = grep("(\\btodo\\b)|á|é|í|ó|ú|ü|ñ", allReviews$allText)

french = grep("(\\je\\b)|(\\ne\\b)|(\\[Uu]ne\\b)|(\\[]\\b)|(\\bgoed\\b)|(\\bniet\\b)|â|ê|î|ô|û", allReviews$allText)

allReviews = allReviews[-c(germans, spanish, french), ]