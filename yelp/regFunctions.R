library(tm)
library(wordcloud)
library(caret)
library(MASS)

build.wordcloud <- function(doc.term.matrix, colors=brewer.pal(9, "Paired")) {
	freqs <- sort(colSums(as.matrix(doc.term.matrix)), decreasing = TRUE)
	words <- names(freqs)
	wordcloud(words, freqs, random.order=FALSE,  
		  use.r.layout=FALSE, colors=colors)
}

#build.wordcloud(sparsedtm, colors=brewer.pal(4, "Set3"))

# Build a dataset from the specified file. The target is "target.stars"
build.dataset <- function(filepath, sparsity.cutoff = 0.98, min.word.length = 3) {
	dtm.control <- list(
		tolower = TRUE, 
		removePunctuation = TRUE,
		removeNumbers = TRUE,
		stopwords = stopwords("english"),
		stemming = TRUE, # false for sentiment
		#weighting = function(x){weightTfIdf(x, normalize = FALSE)},
		minDocFreq = 5,
		wordLengths = c(min.word.length, "inf"))

	d1 <- read.csv(filepath)
	d1$text <- as.character(d1$text)
	d1 <- subset(d1, nchar(text) >= min.word.length)
	corp <- Corpus(VectorSource(d1$text))
	dtm <- DocumentTermMatrix(corp, control = dtm.control)
	sparsedtm <- removeSparseTerms(dtm, sparsity.cutoff)
	dtm.df <- as.data.frame(as.matrix(sparsedtm))
	dtm.df$target.stars <- as.numeric(d1$stars)
	dtm.df
}

# Construct the model.
build.model <- function(training.data) {
	# Build the model
	start.time <- Sys.time()
	modelFit <- train(target.stars ~ .,data=training.data, method="lm")
	#fit <- lm(target.stars ~ .,data=training.data)
	#modelFit <- stepAIC(fit, direction="backward")
	end.time <- Sys.time()
	message(paste("Model Build - Elapsed Time:", end.time - start.time))
	modelFit
}

test.model <- function(dataset, trainp = 0.7) {
	# Build train and test datasets
	set.seed(32343)
	inTrain <- createDataPartition(y = dataset$target.stars, p = trainp, list = FALSE)
	training <- dataset[inTrain,]
	testing <- dataset[-inTrain,]	
	#message(paste("Same levels:", identical(levels(training$target.stars), levels(testing$target.stars))))
	modelFit <- build.model(training)
	message(class(modelFit))
	# Make predictions using test set and assess performance
	predictions <- predict(modelFit, newdata=testing)
	#head(predictions)
	comparisons <- data.frame(actual=testing$target.stars, predicted=predictions, 
							 resids=(predictions-testing$target.stars))
	plot(comparisons$actual, comparisons$predicted)
	#summary(modelFit)
	
	#print(confusionMatrix(predictions, testing$target.stars))
	#message(paste("All Done! Starting and ending times:", start.time, end.time))
	modelFit
}
