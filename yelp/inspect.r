# Good reference: http://www.r-bloggers.com/better-handling-of-json-data-in-r/
library(jsonlite)

get.json <- function(text.lines) {
	s <- text.lines[1]
	i <- 2
	while(i <= length(text.lines)) {
		s <- paste(s, ',', text.lines[i], sep = '')
		i <- i + 1
	}
	fromJSON(paste('[', s, ']'))
}

#user.lines <- stream_in(file("yelp_academic_dataset_user.json"))
#user.lines <- readLines("yelp_academic_dataset_user.json")
#users <- fromJSON(user.lines)
# users <- fromJSON(paste('[', paste(user.lines, sep = ',', collapse = ""), ']'))

user.lines <- readLines("data/yelp_academic_dataset_user.json")
maxf <- 0
u <- -1
for(ul in user.lines) {
	js <- fromJSON(ul)
	#if(js$complements$funny > maxf) {maxf <- js$complements$funny; u <- js$name}
	if(!is.na(js$complements$funny) & (js$complements$funny > 10000)) {message(js$name)}
}