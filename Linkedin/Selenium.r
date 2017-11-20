library('RSelenium')
driver<- rsDriver()
remDr <- driver[["client"]]
remDr$navigate("http://www.linkedin.com/in/dietererben/")
remDr$getCurrentUrl()
remDr$goBack()
webElem <- remDr$findElement(using = 'class', "login-email")
#webElem$getElementAttribute("id")
webElem$highlightElement()
webElem$sendKeysToElement(list("erbendieter96@gmail.com"))
webElem <- remDr$findElement(using = 'class', "login-password")
webElem$sendKeysToElement(list("HanShot1stLinkedin",key="enter"))
webElem <- remDr$findElement(using = 'id', value = "extended-nav-search")

# This didn't work
webElem$sendKeysToElement(list("Hans Erben"))

class=type-ahead-input

name="og:description"

remDr$navigate("http://www.google.com")
webElem <- remDr$findElement(using = "css", "[name = 'q']")
webElem$sendKeysToElement(list("Notre Dame", key = "enter"))

webElems <- remDr$findElements(using = 'css selector', "h3.r")
resHeaders <- unlist(lapply(webElems, function(x){x$getElementText()}))
resHeaders


#To stop it
remDr$close()
#To stop server
driver[["server"]]$stop()

##########
elem <- remDr$findElement(using="id", value="tbody") # get big table in text string
elem$highlightElement() # just for interactive use in browser.  not necessary.
elemtxt <- elem$getElementAttribute("outerHTML")[[1]] # gets us the HTML
elemxml <- htmlTreeParse(elemtxt, useInternalNodes=T) # parse string into HTML tree to allow for querying with XPath
fundList <- unlist(xpathApply(elemxml, '//input[@title]', xmlGetAttr, 'title')) # parses out just the fund name and ticker using XPath
master <- c(master, fundList) # append fund lists from each page together


# Doesn't work anymore.
checkForServer() # search for and download Selenium Server java binary.  Only need to run once.
startServer() # run Selenium Server binary
remDr <- remoteDriver(browserName="firefox", port=4444) # instantiate remote driver to connect to Selenium Server
remDr$open(silent=T) # open web browser