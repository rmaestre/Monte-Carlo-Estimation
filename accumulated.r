library('ggplot2')
data_accumulated<-read.csv('/tmp/accumulated.tsv', header=TRUE, sep='\t')
ggplot(data_accumulated, aes(x=cost, y=probability)) + geom_point()