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
  scale_x_continuous(trans='log10')+
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

# DFA accuracy



fig3 = (package|no_feats)/
  (plot_spacer()|language)

fig3

ggsave(file.path(out_folder,'fig3_analysis.pdf'),fig1, width = 8, height =10)
ggsave(file.path(out_folder,'fig3_analysis.png'),fig1, width = 8, height =10)

#### Supplementary

# Number of features
data_file =  "data/merged_dfa.csv"
dfa_df <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

dfa_acc = ggplot(dfa_df, aes(performance)) +
  geom_histogram(binwidth=2.5)+
  labs(y ='Number of studies', x='Accuracy')+
  theme_classic()
dfa_acc

acc_vs_no = ggplot(dfa_df, aes(x= no_clust, y=performance)) +
  geom_point()+
  labs(x ='Number of types', y='Accuracy')+
  theme_classic()
acc_vs_no

dfa_plot = dfa_acc+acc_vs_no

ggsave(file.path(out_folder,'sfig_dfa.pdf'),dfa_plot, width = 8, height =5)
ggsave(file.path(out_folder,'sfig_dfa.png'),dfa_plot, width = 8, height =5)
