library(ggplot2)
library(patchwork)
library(forcats)
library(dplyr)

out_folder = "figs"
 
data_file =  "data/merged_data.csv"
df_ori <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

df = df_ori[!duplicated(df_ori$Rayyan.ID), ]

# Year published
year = ggplot(df, aes(Year)) +
  geom_histogram()+
  labs(y ='Number of studies', x='Year of publication')+
  theme_classic()
year

# Orders count
orders = ggplot(df_ori, aes(x = fct_infreq(Order), fill=fct_infreq(Order))) +
  geom_bar()+
  labs(y ='Number of studies', x='Order', fill='Order')+
  theme_classic()+theme(axis.text.x=element_text(angle = 45, vjust = 1.0, hjust=1))
orders
temp = fct_infreq(df_ori$Order)
# Open Access
open_access = ggplot(df, aes(x = fct_infreq(Open.access), fill=Open.access)) +
  geom_bar()+
  labs(y ='Count', x='Open Access', fill='Open Access')+
  theme_classic()+ theme(legend.position="none")
open_access

table(df$Open.access)

# Data freely available
data_avail = ggplot(df, aes(x = fct_infreq(Data.availability), fill=fct_infreq(Data.availability))) +
  geom_bar()+
  labs(y ='Number of studies', x='Data availability', fill='Data availability')+
  theme_classic()+ theme(legend.position="none")+theme(axis.text.x=element_text(angle = 45, vjust = 1.0, hjust=1))
data_avail
table(df$Data.availability)


df$open_access = 0
df[df$Open.access=='Yes',]$open_access = 1
open_access_grouped = df %>%
  group_by(Year) %>%
  summarize(Mean = mean(open_access, na.rm=TRUE))
open_access_grouped$Mean = open_access_grouped$Mean*100

open_access_time = ggplot(open_access_grouped, aes(x = Year, y=Mean)) +
  geom_point()+
  labs(x ='Year', y='Open access papers (%)')+
  theme_classic()
open_access_time


df$data_available = 1
df[df$Data.availability=='No',]$data_available = 0
data_grouped = df %>%
  group_by(Year) %>%
  summarize(Mean = mean(data_available, na.rm=TRUE))

data_grouped$Mean = data_grouped$Mean*100
data_avail_time = ggplot(data_grouped, aes(x = Year, y=Mean)) +
  geom_point()+
  labs(x ='Year', y='Data available (%)')+
  theme_classic()
data_avail_time

fig1 = (year|orders)/
  (open_access|data_avail)/
  (open_access_time|data_avail_time)
fig1

ggsave(file.path(out_folder,'fig1_record_chars.pdf'),fig1, width = 8, height =10)
ggsave(file.path(out_folder,'fig1_record_chars.png'),fig1, width = 8, height =10)


##################################################################################
## Supplementary
## Species per order
data_file =  "data/species_per_order.csv"
df_spo <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)
order_order = levels(temp)
species_per_order = ggplot(df_spo, aes(y=unique_species, x = factor(Order, order_order), fill=factor(Order, order_order))) +
  geom_bar(stat="identity")+
  labs(y ='Number of species', x='Order', fill='Order')+
  theme_classic()+theme(axis.text.x=element_text(angle = 45, vjust = 0.8, hjust=1))+ theme(legend.position="none")
species_per_order



df['combine_journal'] = df['journal']
levels(df$combine_journal) <- c(levels(df$combine_journal),"Other")
dt = table(df$journal)
single_journal = rownames(dt)[dt<3]
df$combine_journal[df$journal %in% single_journal] <- 'Other'
journal = ggplot(df, aes(x = fct_infreq(combine_journal), fill=fct_infreq(combine_journal))) +
  geom_bar()+
  labs(y ='Count', x='Journal', fill='Journal')+
  theme_classic()+theme(axis.text.x=element_blank())
journal

sfig = (species_per_order)
sfig

ggsave(file.path(out_folder,'sfig_order_and_journal.pdf'),sfig, width = 8, height =5)
ggsave(file.path(out_folder,'sfig_order_and_journal.png'),sfig, width = 8, height =5)

