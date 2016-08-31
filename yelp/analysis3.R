# This is the main model-building. The saved workspace came from this.
source('classFunctions.R')
library(caret)

message('Building Dataset...')
curr.data <- balanced.traintest.data("review_data_100k.csv", 25000, trainp=0.7, sparsity.cutoff = 0.93) 
#curr.data <- balanced.traintest.data("review_data_15k.csv", 5000, trainp=0.7, sparsity.cutoff = 0.93) # Smaller test example
message('Building Model Stack...')
inSub <- createDataPartition(y = curr.data$training$target.stars, p = 0.6, list = FALSE)
train.sub <- curr.data$training[inSub,]
train.top <- curr.data$training[-inSub,]
stack.predictf <- model.stack.predictorf(train.sub, train.top, top.model="rf", sub.models=c("qda","gbm","rf"))
head(stack.predictf(curr.data$testing))
print(confusionMatrix(stack.predictf(curr.data$testing), curr.data$testing$target.stars))