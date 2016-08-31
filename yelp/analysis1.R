#Needed <- c("tm", "SnowballC", "RColorBrewer", "ggplot2", "wordcloud", "biclust", "cluster", "igraph", "fpc", "caret")   
#install.packages(Needed, dependencies=TRUE)   
# install.packages('wordcloud')
#install.packages("Rcampdf", repos = "http://datacube.wu.ac.at/", type = "source") 
library(tm)
library(wordcloud)
library(caret)

min.word.length <- 3

dtm.control <- list(
	tolower = TRUE, 
	removePunctuation = TRUE,
	removeNumbers = TRUE,
	stopwords = stopwords("english"),
	stemming = TRUE, # false for sentiment
	weighting = function(x){weightTfIdf(x, normalize = FALSE)},
	minDocFreq = 5,
	wordLengths = c(min.word.length, "inf"))


d1 <- read.csv("review_data_15k.csv")
d1$text <- as.character(d1$text)
d1 <- subset(d1, nchar(text) >= min.word.length)
corp <- Corpus(VectorSource(d1$text))
dtm <- DocumentTermMatrix(corp, control = dtm.control)
sparsedtm <- removeSparseTerms(dtm, 0.98)
dtm.df <- as.data.frame(as.matrix(sparsedtm))
head(dtm.df)
dim(dtm.df)

freqs <- sort(colSums(as.matrix(sparsedtm)), decreasing = TRUE)
head(freqs)
words <- names(freqs)
# wordcloud(words, freqs,  random.order=FALSE, #rot.per=0.35, 
		  # use.r.layout=FALSE, colors=brewer.pal(4, "Dark2"))
# wordcloud(words, freqs,  random.order=FALSE, #rot.per=0.35, 
		  # use.r.layout=FALSE, colors=brewer.pal(9,"BuGn"))
# wordcloud(words, freqs,  random.order=FALSE, #rot.per=0.35, 
		  # use.r.layout=FALSE, colors=brewer.pal(4, "Set3"))
# wordcloud(words, freqs,  random.order=FALSE, #rot.per=0.35, 
		  # use.r.layout=FALSE, colors=brewer.pal(9, "Paired"))

build.wordcloud <- function(doc.term.matrix, colors=brewer.pal(9, "Paired")) {
	freqs <- sort(colSums(as.matrix(doc.term.matrix)), decreasing = TRUE)
	words <- names(freqs)
	wordcloud(words, freqs, random.order=FALSE,  
		  use.r.layout=FALSE, colors=colors)
}

build.wordcloud(sparsedtm, colors=brewer.pal(4, "Set3"))


ds <- build.dataset("review_data_15k.csv")
test.model(ds)
test.model(ds[sample(1:nrow(ds), 3000),])
test.model(ds[sample(1:nrow(ds), 3000),], method="qda") # fast
test.model(ds[sample(1:nrow(ds), 3000),], method="ranger")

ds2 <- build.dataset("review_data_100k.csv", sparsity.cutoff=0.93)
bs2 <- balanced.sample(ds2, 25000)
qda.results.25k <- test.model(bs2, method="qda")
gbm.results.25k <- test.model(bs2, method="gbm")

