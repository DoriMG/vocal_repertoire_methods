library(ggplot2)
library(patchwork)
library(forcats)
library(dplyr)

out_folder = "figs"


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

# What features are used?
data_file =  "data/features_included_manual.csv"
feat_type_df <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE, sep=';')

no_feats = ggplot(no_feats_df, aes(features)) +
  geom_histogram()+
  labs(y ='Number of studies', x='Number of features')+
  theme_classic()
no_feats

# What analysis package is used
data_file =  "data/analysis_programs.csv"
analysis_df <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

analysis_df$combine_package = analysis_df$package
levels(analysis_df$combine_package) <- c(levels(analysis_df$combine_package),"Other")
dt = table(analysis_df$package)
single_package = rownames(dt)[dt<3]
analysis_df$combine_package[analysis_df$package %in% single_package] <- 'Other'

language = ggplot(analysis_df, aes(x = fct_infreq(combine_package), fill=fct_infreq(combine_package))) +
  geom_bar()+
  labs(y ='Count', x='Package', fill='Package')+
  theme_classic()+ theme(legend.position="none")+theme(axis.text.x=element_text(angle = 45, vjust = 1.0, hjust=1))

language

# Analysis type


fig1 = (package|no_feats)/
  (language|data_avail)/
  (open_access_time|data_avail_time)
fig1

ggsave(file.path(out_folder,'fig3_analysis.pdf'),fig1, width = 8, height =10)
ggsave(file.path(out_folder,'fig3_analysis.png'),fig1, width = 8, height =10)