source('classFunctions.R')
library(caret)

#ds <- build.dataset("review_data_100k.csv")
#test.model(ds)
#test.model(ds[sample(1:nrow(ds), 3000),])
#test.model(ds[sample(1:nrow(ds), 3000),], method="qda") # fast
#test.model(ds[sample(1:nrow(ds), 3000),], method="ranger")

# message('Building Dataset...')
# ds2 <- build.dataset("review_data_100k.csv", sparsity.cutoff=0.93)
# message('Getting Balanced Sample...')
# bs2 <- balanced.sample(ds2, 25000)
# message('Building QDA model...')
# qda.results.25k <- test.model(bs2, method="qda")
# message('Building GBM model...')
# gbm.results.25k <- test.model(bs2, method="gbm")

# message('Building Dataset...')
# curr.data <- balanced.traintest.data("review_data_100k.csv", 25000, sparsity.cutoff = 0.93) 
# message('Building Model Stack...')
# stack.results.25k <- model.stack(curr.data$training, curr.data$testing, base.model="rf", models=c("qda","gbm"))

message('Building Dataset...')
curr.data <- balanced.traintest.data("review_data_100k.csv", 5000, trainp=0.7, sparsity.cutoff = 0.93) 
message('Building Model Stack...')
inSub <- createDataPartition(y = curr.data$training$target.stars, p = 0.6, list = FALSE)
train.sub <- curr.data$training[inSub,]
train.top <- curr.data$training[-inSub,]
stack.predictf <- model.stack.predictorf(train.sub, train.top, top.model="rf", sub.models=c("qda"))
head(stack.predictf(curr.data$testing))
print(confusionMatrix(stack.predictf(curr.data$testing), curr.data$testing$target.stars))

