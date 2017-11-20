#####################
### Workshop Code ###
#####################

### R Install ###
# Not in the presentation, but might be handy for you.
# R: https://cloud.r-project.org/
# RStudio: https://www.rstudio.com/products/rstudio/download/#download

# Briefly, you can do everything you would ever need with R alone.
# RStudio is an IDE that makes working with R easier. You get a
# scripting environment, package manager, viewers, etc. While I
# might not have earned it, please just trust me that it will make
# learning R much easier. I learned it the old-school way and have
# the brain damage to show for it.

### Package Installation ###

# The easiest way to run a line of code is to put your cursor
# anywhere on the line and press Control + Enter. If we have a
# piped chunk (this will become clear later), then you can put
# your cursor anywhere on the chunk and run it. There is almost
# never a need to highlight everything to run it.

install.packages(c('tidyverse', 'plotly', 'DT', 'data.table'))

# You will only ever need to run the previous line once (unless you update R).

### The Basics ###

numList = 1:5

numList

### The Functions ###

nonsenseFunction = function(x) {
  res = (sqrt(x) + sin(x))^2
  return(res)
}

test = 1:10

nonsenseFunction(test)

# Just to show you, we could also do something like the following:

nonsenseFunction(1:10)

# We did not create an object, but just passed a vector into
# our function. We can compound things like this:

nonSenseOutput = nonsenseFunction(test)

# So, we have created a new object using our test object and our function!

### Our Data ###

library(rvest); library(xml2); library(magrittr)

filmLink = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

allTables = read_html(filmLink) %>%
  html_table(fill = TRUE)

highestGrossing = allTables %>%
  extract2(1)

head(highestGrossing)

# You may want to see all of your data -- use View(highestGrossing)
# This is an important note to make: R is case sensitive.
# Be honest -- you typed View() with a lowercase "v", right?
# If you didn't make that mistake, then pat yourself on the back.

### Action! (Or using select) ###

highestGrossing = highestGrossing %>%
  select(-Rank, -`Reference(s)`)

head(highestGrossing)

### String Cleaning ###

library(stringr)

highestGrossing = highestGrossing %>%
  mutate(Peak = str_replace(Peak, "[A-Z].*", ""),
         Peak = as.numeric(Peak),
         gross = as.numeric(str_replace_all(`Worldwide gross`, "\\$|,", ""))) %>%
  select(-`Worldwide gross`)

### Filter ###

highestGrossing = highestGrossing %>%
  filter(Peak != 1 & Peak != max(Peak))

### GDP Deflator ###

gdpDeflator2017 = read_html("http://www.multpl.com/gdp-deflator/table") %>%
  html_table(trim = TRUE, header = TRUE) %>%
  extract2(1) %>%
  filter(grepl("2017", Date) == TRUE) %>%
  select(-Date) %>%
  extract2(1)

### Using Mutate ###

highestGrossing = highestGrossing %>%
  mutate(grossReal2017 = gross/(gdpDeflator2017/100))

### Group_by ###

highestGrossing = highestGrossing %>%
  group_by(Year)

### Summarize ###

highestGrossingSummary = highestGrossing %>%
  summarize(n = n(),
            meanGross = mean(grossReal2017))

head(highestGrossingSummary)

### Coding How We Think ###

allTables = read_html(filmLink) %>%
  html_table(fill = TRUE) %>%
  extract2(1) %>%
  select(-Rank, -`Reference(s)`) %>%
  mutate(Peak = str_replace(Peak, "[A-Z].*", ""),
         Peak = as.numeric(Peak),
         gross = as.numeric(str_replace_all(`Worldwide gross`, "\\$|,", ""))) %>%
  select(-`Worldwide gross`) %>%
  filter(Peak != 1 & Peak != max(Peak)) %>%
  mutate(grossReal2017 = gross/(gdpDeflator2017/100)) %>%
  group_by(Year) %>%
  summarize(n = n(),
            meanGross = mean(grossReal2017))


# Are you still here, after all this time?
# I am proud of you! Not only am I proud of
# you, but so is Bill "The Wizard" Venables.
# If you have made it here, without tears,
# speak now (yes, right now -- I am probably
# not saying anything too important) to
# get your pick of R t-shirts. Be fast, though,
# because it will only go to one person.

### An Interactive Look ###

library(DT)

datatable(highestGrossingSummary)

### Visual Exploration ###

library(ggplot2)

ggplot(highestGrossingSummary, aes(Year, meanGross, size = n)) +
  geom_point() +
  theme_minimal()

# If this is your first exposure to ggplot2, then it
# might seem daunting -- just know that it isn't.
# You can do things with ggplot2 that you never thought
# possible. With regard to a typical plot, I went pretty
# sparse here, but do know that the sky is the limit and
# we can build layers upon layer.

### Something A Bit More Modern ###

movieByYear = highestGrossing %>%
  group_by(Year) %>%
  dplyr::summarise(movies = paste(Title, collapse = "\n")) %>%
  right_join(., highestGrossingSummary, by = "Year")

library(plotly)

p = ggplot(movieByYear, aes(Year, meanGross, size = n, color = meanGross)) +
  geom_point(aes(text = movies)) +
  theme_minimal() +
  theme(axis.text.y=element_blank(),
        axis.title.y=element_blank())

ggplotly(p, tooltip = c("text", "size", "color"))

### Coalesce ###

testDF = data.frame(x1 = c(1:5, rep(NA, 5)),
                    x2 = c(rep(NA, 5), 6:10))

testDF

testDF %>%
  mutate(z = coalesce(x1, x2))

# The first person to yell their favorite
# dplyr function gets to pick the next shirt.
# If you start a slow-clap/chant, I will throw
# in a pick from the candy bag; I see no reason
# why I should be the only person looking foolish.

### Parting Thoughts ###

# I wish that we had the time to get into many other things, but
# we don't. Do know, however, that dplyr makes joining data frames
# simple (left_join, right_join, inner_join, full_join, anti_join)
# and it has a ton of other functions. Similarly, the tidyr package
# makes reshaping data a breeze (wide to long, long to wide, and some
# other handy features for splitting and joining columns). Finally, while
# not part of the tidyverse, the data.table package is great for larger
# data issues. The syntax is wacky, but it can do a lot of neat things.