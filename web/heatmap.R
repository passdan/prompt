library("gplots")
data <- read.csv("/var/www/metamod/tmp/compound_abun.csv", header=TRUE, row.names = 1)
names(data)
data<-log(data+1)
data_matrix <-data.matrix(data)
pdf('./tmp/current.pdf');

hv <- heatmap.2(data_matrix, col=rev(heat.colors(155)), scale="none",
                margin=c(5, 10), trace="none", density="density")
