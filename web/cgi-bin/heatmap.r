#!/usr/bin/R

library("gplots")

data <- read.table("/var/www/prompt/tmp/current_selection.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
row.names(data)<-data[,1]
data<-data[,-1]
data_matrix <-data.matrix(data)

breaks=seq(0, 75, by=5)
breaks=append(breaks, 100)
mycol <- colorpanel(n=length(breaks)-1,low="#F0F0F0",mid="black",high="red")

png("/var/www/prompt/tmp/heatmap.png",width=3000,height=2500,res=300)
hv <- heatmap.2(data_matrix, col=mycol, scale="none",
         margin=c(10, 12),
	 density.info="histogram",
	 breaks=breaks,
         xlab="Sample", ylab= "Taxa",
         trace="none", dendrogram=c("column"))
dev.off()
