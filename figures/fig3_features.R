library(ggplot2)
library(patchwork)
library(forcats)
library(dplyr)

out_folder = "figs"

data_file =  "data/merged_data.csv"
df_ori <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

df = df_ori[!duplicated(df_ori$Rayyan.ID), ]
df = df[df$Language!= 'N/A',]
df = df[df$analysis_methods!= '',]

write.csv(df,"data/analysis_df.csv", row.names = FALSE)


# Package
data_file =  "data/packages.csv"
packages_df <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

packages_df$combine_package = packages_df$package
levels(packages_df$combine_package) <- c(levels(packages_df$combine_package),"Other")
dt = table(packages_df$package)
single_package = rownames(dt)[dt<3]
packages_df$combine_package[packages_df$package %in% single_package] <- 'Other'

package = ggplot(packages_df, aes(x = fct_infreq(combine_package), fill=fct_infreq(combine_package))) +
  geom_bar()+
  labs(y ='Count', x='Package', fill='Package')+
  theme_classic()+ theme(legend.position="none")+theme(axis.text.x=element_text(angle = 45, vjust = 1.0, hjust=1))

package

# Number of features
data_file =  "data/no_features.csv"
no_feats_df <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

no_feats = ggplot(no_feats_df, aes(features)) +
  geom_histogram()+
  labs(y ='Number of studies', x='Number of features')+
  theme_classic()
no_feats
