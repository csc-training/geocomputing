#Example from: https://www.rdocumentation.org/packages/raster/versions/2.5-8/topics/predict

# A simple model to predict the location of the R in the R-logo using 20 presence points 
# and 50 (random) pseudo-absence points. This type of model is often used to predict
# species distributions. See the dismo package for more of that.

library(raster)
setwd("raster_predict")

# create a RasterStack or RasterBrick with with a set of predictor layers
logo <- brick("rlogo.grd")
names(logo)

# known presence and absence points
p <- matrix(c(48, 48, 48, 53, 50, 46, 54, 70, 84, 85, 74, 84, 95, 85, 
   66, 42, 26, 4, 19, 17, 7, 14, 26, 29, 39, 45, 51, 56, 46, 38, 31, 
   22, 34, 60, 70, 73, 63, 46, 43, 28), ncol=2)

a <- matrix(c(22, 33, 64, 85, 92, 94, 59, 27, 30, 64, 60, 33, 31, 9,
   99, 67, 15, 5, 4, 30, 8, 37, 42, 27, 19, 69, 60, 73, 3, 5, 21,
   37, 52, 70, 74, 9, 13, 4, 17, 47), ncol=2)


# extract values for points
xy <- rbind(cbind(1, p), cbind(0, a))
v <- data.frame(cbind(pa=xy[,1], extract(logo, xy[,2:3])))

#build a model, here an example with glm 
model <- glm(formula=pa~., data=v)

#Serial code for making predictions:
#r1 <- predict(logo, model, progress='text')

#Run predict function using an mpi cluster. Note that in taito the cluster is already available, you shouldn't start it yourself but use the handle provided by getMPIcluster.
cl<-getMPIcluster()
r1 <- clusterR(logo, predict, args=list(model), cl=cl)
stopCluster(cl)


#Plot the original data and results
plotRGB(logo)
points(p, bg='blue', pch=21)
points(a, bg='red', pch=21)
plot(r1,col = gray.colors(10, start = 0, end = 1, gamma = 1, alpha = NULL))
quit()

