#!/usr/bin/R

library("vegan")
library("ggplot2")

x <- read.table("/var/www/prompt/tmp/current_selection.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)

x<-x[,-1]

#Make MDS
x_matrix <- t(x)
x.mds <- metaMDS(x_matrix, trace = FALSE)

png("/var/www/prompt/tmp/nmds.png",width=3000,height=2500,res=300)
plot(x.mds, type = "t")
dev.off()
