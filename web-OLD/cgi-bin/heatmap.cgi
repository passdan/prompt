#!/usr/bin/R

library("gplots")
data <- read.table("/var/www/metamod/Diatoms/abundance/compound_abun.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
names(data)
row.names(data)<-data$OTU.ID
data<-data[,2:4]
data_matrix <-data.matrix(data)

hv <- heatmap.2(data_matrix, col=rev(heat.colors(155)), scale="none",
                 margin=c(5, 10),
               xlab="individual", ylab= "OTU",
               main="heatmap(Comparison of selected sites, scale=\"column\")",
         trace="none", density="density")
