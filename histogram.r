library('ggplot2')
data<-read.csv('/tmp/histogram.tsv', header=TRUE, sep='\t')
ggplot(data, aes(x=cost)) + geom_histogram(binwidth = 10)