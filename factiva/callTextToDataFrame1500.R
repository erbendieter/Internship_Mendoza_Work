load("C:/Users/Dieter Erben/desktop/callsRawComp.RData")

#Question-and-Answer Session Presentation

#initial = as.data.frame(as.list(bigList$BBBY_2013_3))

library(dplyr); library(tidyr)

callTextToDataFrame = function(callText){

  out = tryCatch({

    #initial = callText

    #initial = as.data.frame(unlist(lapply(as.list(callText), function(x) rvest::repair_encoding(x))))

    initial = as.data.frame(as.list(callText))

    names(initial) = "."

    initial$. = as.character(initial$.)

    initial$. = stringr::str_trim(initial$.)

    analystTest = initial[(which(grepl("^Analyst(s)?", initial$.))) - 1, ]

    execs = if(length(analystTest) == 0) {
      initial[(which(grepl("^Executive(s)?", initial$.)) + 1):
                (which(grepl("^Operator", initial$.))) - 1, ]
    } else {
      initial[(which(grepl("^Executive(s)?", initial$.)) + 1):
                (which(grepl("^Analyst(s)?", initial$.))) - 1, ]
    }


    execs = gsub("^Executive(s)?", NA, execs)

    execs[which(execs == "")] = NA

    execs = na.omit(execs)

    initial$.[which(initial$. %in% execs)] = stringr::str_extract(execs, "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|^(\\w+) (\\w+\\. ){1,5}(\\w+)|(\\w+) (\\w+\\.){1,5}( \\w+)$|(\\w+) (\\w+)")
    
    execs = stringr::str_extract(execs, "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+) (\\w+)|(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|^(\\w+) (\\w+\\. ){1,5}(\\w+)|(\\w+) (\\w+\\.){1,5}( \\w+)$|(\\w+) (\\w+)")

    execs = unique(append(execs,sub('(\\w+) (\\w+\\. ){1,5}(\\w+)','\\1 \\3', execs)))
    execs = unique(append(execs,sub('(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)','\\1 \\3', sub('Jr\\.|II|III|IV|V','',execs))))
    execs = gsub("^\\s+|\\s+$", "", execs)
    execs = sub('\\s{2}','\\s{1}',execs)
    
    initial$. = stringr::str_trim(initial$.)

    if(length(analystTest) != 0){

      analysts = initial[(which(grepl("^Analyst(s)?", initial$.)) + 1):
                           match("Operator", initial$.) - 1, ]

      analysts = gsub("Analysts", NA, analysts)

      analysts[which(analysts == "")] = NA

      analysts = na.omit(analysts)

      initial$. = as.character(initial$.)

      initial$.[which(initial$. %in% analysts)] = stringr::str_extract(analysts, "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|^(\\w+) (\\w+\\. ){1,5}(\\w+)|(\\w+) (\\w+\\.){1,5}( \\w+)$|(\\w+) (\\w+)")
      
      analysts = stringr::str_extract(analysts, "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+) (\\w+)|(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|^(\\w+) (\\w+\\. ){1,5}(\\w+)|(\\w+) (\\w+\\.){1,5}( \\w+)$|(\\w+) (\\w+)")
      
      analysts = unique(append(analysts,sub('(\\w+) (\\w+\\. ){1,5}(\\w+)','\\1 \\3', analysts)))
      analysts = unique(append(analysts,sub('(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)','\\1 \\3', sub('Jr\\.|II|III|IV|V','',analysts))))
      analysts = gsub("^\\s+|\\s+$", "", analysts)
      analysts = sub('\\s{2}','\\s{1}',analysts)
      
      #initial$.[which(initial$. %in% analysts)] = stringr::str_extract(initial$.[which(initial$. %in% analysts)], "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|\\w* [a-zA-Z]..\\w*|\\w* \\w* \\w*|\\w* \\w*||(\\w+) (\\w+)")

      #analysts = stringr::str_extract(analysts, "(\\w+) ([A-Z]\\.[A-Z]\\.) (\\w+)|\\w* [a-zA-Z]..\\w*|\\w* \\w* \\w*|\\w* \\w*||(\\w+) (\\w+)")
      #analysts = unique(append(analysts,sub('^(\\w+) (\\w+\\. ){1,5}(\\w+)|(\\w+) (\\w+\\.){1,5}( \\w+)$', '\\1 \\4', analysts)))
      #analysts = sub('\\s{2}','\\s{1}',analysts)
      #analysts = sub('Jr\\.|II|III|IV|V','',analysts)
    }

    allPeople = if(length(analystTest) == 0) {
      execs
    } else {c(analysts, execs)}

    initial$.[which(initial$. == "")] = NA

    initial = na.omit(initial)

    # initial$.[grep("^Operator", initial$.) + 1] = ""
    #
    # initial$.[grep("^Operator", initial$.)] = ""

    initial$role = if(length(analystTest) == 0) {
      ifelse(initial$. %in% execs == TRUE, "exec", "")
    } else {
      ifelse(initial$. %in% execs == TRUE, "exec",
             ifelse(initial$. %in% analysts == TRUE, "analyst", ""))
    }

    initial$role = ifelse(initial$. == "Operator", "operator", initial$role)

    initial$.[which(initial$. == "")] = NA

    initial = na.omit(initial)

    initial[, 3] = initial[, 1]

    initial[, 3] = as.character(initial[, 3])

    initial$callPart = ifelse(grepl("Question(s)?.[Aa]nd.Answer", initial$.),
                              "QA",
                              NA)

    names(initial) = c("text", "role", "name", "callPart")

    initial$name = ifelse(initial$name %in% allPeople == TRUE, initial$name, "")

    initial$name = ifelse(initial$role == "operator", "operator", initial$name)

    initial$text = ifelse(initial$text %in% allPeople == TRUE, "", initial$text)

    initial$name = dplyr::lag(initial$name)
    initial$role = dplyr::lag(initial$role)
    initial$callPart = dplyr::lag(initial$callPart, 2)

    initial$text[which(initial$text == "Operator")] = ""

    initial = initial[initial$text != "", ]

    initial$callPart[1] = "Intro"

    initial = initial %>%
      fill_(c("callPart"))

    initial[grep("^Executive(s)?", initial$text), ] = NA

    initial[grep("^Analyst(s)?", initial$text), ] = NA

    initial = na.omit(initial)

    initial = initial %>% mutate(seqNum = seq(from = 1, to = nrow(initial)) * .001,
                                 nameSeq = ifelse(nchar(name) > 3,
                                                  paste(seqNum, name, role, callPart, sep = ":"),
                                                  NA)) %>%
      fill(nameSeq) %>%
      group_by(nameSeq) %>%
      summarize(text2 = paste(text, collapse = " ")) %>%
      arrange() %>%
      separate(nameSeq, into = c("num", "name", "role", "callPart"), sep = ":", remove = TRUE) %>%
      select(-num)

  },
  error=function(cond) {
    message(paste("Call does not exist:", callText))
    #message(cond)
    return(NA)
  }

  )

  return(out)

}

debugonce(callTextToDataFrame)

initial = bigList[1]

test = callTextToDataFrame(initial)

bigList$NA_NA_NA = NULL

test = rep(list(list()), length(bigList))

test = lapply(bigList, function(x) callTextToDataFrame(x))

save(test, file = "data/ticks1500RevisedCallDFs.RData")
