library(ggplot2)

##ACCURACY##
acc_df <- read.csv("accuracy_df.csv", sep=",", header=TRUE)
acc_df$form <- as.factor(acc_df$type)
acc_df$authenticity <- as.factor(acc_df$truth)

#Data Visualization
hist(acc_df$accuracy, col = "red")

ggplot(data=acc_df, aes(x=form, y=accuracy, fill=form)) + 
  geom_violin() + geom_boxplot(width=0.1)

ggplot(data=acc_df, aes(x=authenticity, y=accuracy, fill=authenticity)) + 
  geom_violin() + geom_boxplot(width=0.1)

#Total Accuracy (Real and Fake Datapoints)
anova(lm(accuracy~form*authenticity, data=acc_df))
plot(lm(accuracy~form*authenticity, data=acc_df))

#interaction plot
interaction.plot(x.factor=acc_df$authenticity, 
                 trace.factor = acc_df$form,
                 response = acc_df$accuracy, 
                 fun=mean, type='b')

#Normality tests
shapiro.test(acc_df$accuracy)



##RESPONSE TIME##
rt_df<-read.csv("rt_df.csv", sep=",", header=TRUE)
rt_df$form<-as.factor(rt_df$type)
rt_df$authenticity<-as.factor(rt_df$truth)

#Data Visualization
hist(rt_df$RT, col = "blue")

ggplot(data=rt_df, aes(x=form, y=RT, fill=form)) + 
  geom_violin() + geom_boxplot(width=0.1)

ggplot(data=rt_df, aes(x=authenticity, y=RT, fill=authenticity)) + 
  geom_violin() + geom_boxplot(width=0.1)

#Reaction Time
anova(lm(RT~form*authenticity, data=rt_df))
plot(lm(RT~form*authenticity, data=rt_df))

#interaction plot
interaction.plot(x.factor=rt_df$authenticity, 
                 trace.factor = rt_df$form,
                 response = rt_df$RT, 
                 fun=mean, type='b')

#Normality tests
shapiro.test(rt_df$RT)
