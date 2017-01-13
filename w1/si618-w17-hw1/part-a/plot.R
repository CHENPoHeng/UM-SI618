# setwd('Documents/umsi/SI618/w1/si618-w17-hw1/part-a/')
d = read.csv('worldbank_output_pohechen.csv')
data = d
# header = names(d)
# d = read.csv('si618_w17_hw1a_expected_output.csv')
# names(d) = header
i = which(data$Region %in% c('Europe', 'The Americas') & substr(data$Date,5,8) == '2000')
d = data[i, ]

# plot1: 2000
pdf(file = 'si618-hw1-plot1-2000_pohechen.pdf')
plot(d$Mobile.subscribers.per.capita, d$Business..Internet.users..per.100.people.,
     xlim = c(0,1), ylim = c(0, 60), xlab = 'Mobile users per capita', ylab = 'Internet users per 100 users',
     main = 'Mobile vs internet usage\nfor Europe vs American in year 2000',
     type = 'n')
for(i in c(1,2)){
    tmp = d[which(d$Region == unique(d$Region)[i]), ]
    points(tmp$Mobile.subscribers.per.capita, tmp$Business..Internet.users..per.100.people.,
           col = c('Blue', 'Red')[i], pch = 16)
}
legend('bottomright',legend =  unique(d$Region), col = c('Blue', 'Red'), pch = 16, cex = 0.8)
dev.off()

# plot1: 2010
i = which(data$Region %in% c('Europe', 'The Americas') & substr(data$Date,5,8) == '2010')
d = data[i, ]

pdf(file = 'si618-hw1-plot1-2010_pohechen.pdf')
plot(d$Mobile.subscribers.per.capita, d$Business..Internet.users..per.100.people.,
     xlim = c(0,2), ylim = c(0, 100), xlab = 'Mobile users per capita', ylab = 'Internet users per 100 users',
     main = 'Mobile vs internet usage\nfor Europe vs American in year 2010',
     type = 'n')
for(i in c(1,2)){
    tmp = d[which(d$Region == unique(d$Region)[i]), ]
    points(tmp$Mobile.subscribers.per.capita, tmp$Business..Internet.users..per.100.people.,
           col = c('Blue', 'Red')[i], pch = 16)
}
legend('bottomright',legend =  unique(d$Region), col = c('Blue', 'Red'), pch = 16, cex = 0.8)
dev.off()




# plot2: log(finance) vs log(health)
i = which(data$Region %in% c('Europe', 'Asia', 'The Americas', 'Africa') & substr(data$Date,5,8) == '2010')
d = data[i, ]
pdf(file = 'si618-hw1-plot2_pohechen.pdf')
plot(d$log.GDP.per.capita., d$log.Health..mortality.under.5.,
     xlab = 'log(Finance: GDP per capita)', ylab = 'log(Health: Mortality, under 5)',
     main = 'GDP per capita vs mortality in log in year 2010',
     type = 'n')
for(i in c(1:length(unique(d$Region)))){
    tmp = d[which(d$Region == unique(d$Region)[i]), ]
    points(tmp$log.GDP.per.capita., tmp$log.Health..mortality.under.5.,
           col = i, pch = 16)
}
legend('topright',legend =  unique(d$Region), col = 1:length(unique(d$Region)), pch = 16, cex = 0.8)
dev.off()

