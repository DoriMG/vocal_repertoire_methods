library(ggplot2)
library(patchwork)
library(forcats)

out_folder = "figs"

data_file =  "data/rec_locations.csv"
df_loc <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)
df_loc$percs = df_loc$percs*100
loc_order = c("field", 'lab', 'zoo', 'farm')
recording_location = ggplot(df_loc, aes(y=percs, x = factor(location, loc_order) , fill=factor(location, loc_order)  )) +
  geom_bar(stat="identity")+
  labs(y ='Studies (%)', x='Location', fill='Location')+
  theme_classic()+ theme(legend.position="none")
recording_location

data_file =  "data/contexts.csv"
df_loc <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)
df_loc$percs = df_loc$percs*100
con_order = c("group", 'both', 'solitary')
context = ggplot(df_loc, aes(y=percs, x = factor(context , con_order) , fill=factor(context , con_order)  )) +
  geom_bar(stat="identity")+
  labs(y ='Studies (%)', x='Context')+
  theme_classic()+ theme(legend.position="none")
context

# Number of animals

data_file =  "data/merged_data.csv"
df_ori <- read.csv(data_file, header=TRUE, stringsAsFactors=TRUE)

df_temp = df_ori[df_ori['n_animals']>0,]
n_animals = ggplot(df_temp, aes(n_animals)) +
  geom_histogram(bins = 20)+
  scale_x_continuous(trans='log10')+
  labs(y ='Count', x='Animals N')+
  theme_classic()
n_animals

# Number of vocalizations
df_temp = df_ori[df_ori['n_recs_analysed']>0,]
n_recs_analysed = ggplot(df_temp, aes(n_recs_analysed)) +
  geom_histogram(bins = 20)+
  scale_x_continuous(trans='log10')+
  labs(y ='Count', x='Vocalizations N')+
  theme_classic()
n_recs_analysed

## Trends
animals_over_time = ggplot(df_temp, aes(x = Year, y=n_animals)) +
  geom_point()+
  labs(x ='Year', y='Number of animals')+
  theme_classic()+
  scale_y_continuous(trans='log10')
animals_over_time


recs_over_time = ggplot(df_temp, aes(x = Year, y=n_recs_analysed)) +
  geom_point()+
  labs(x ='Year', y='Number of recordings')+
  theme_classic()+
  scale_y_continuous(trans='log10')
recs_over_time


all_figs =  (recording_location|context)/
  (n_animals|n_recs_analysed)/
  (animals_over_time|recs_over_time)
all_figs


ggsave(file.path(out_folder,'fig2_rec_methods.pdf'),all_figs, width = 8, height =10)
ggsave(file.path(out_folder,'fig2_rec_methods.png'),all_figs, width = 8, height =10)

