# import neccesary libraries
import pandas as pd
import numpy as np

# load the advert_categories.csv data 
advert = pd.read_csv("data/advert_categories.csv", index_col=[0])

# Setting the social media types

# Cleaning the social media column
advert["social_media"] = advert["social_media"].str.replace("-", "")
advert["social_media"] = advert["social_media"].str.replace("/X", "")

# available social media platforms
social_media = ["Facebook", "Instagram", "Twitter", "LinkedIn", 'WhatsApp', "TikTok", "Telegram", "Snapchat"]

# function to count distinct social media used by each repondents
def get_ads(col):
    vals = list(col)
    ads_dict = {i: [] for i in social_media}
    for i in vals:
        ads_list = i.split(", ")
        for ads in ads_dict:
            ads_dict[ads].append(len(set(ads_list) & {ads}))
    return ads_dict


# getting the distinct ads and converting to dataframe
ads_dict = get_ads(advert["social_media"])
ads_df = pd.DataFrame(ads_dict)


# merging both dataframes together
new_advert = pd.merge(advert, ads_df, left_index=True, right_index=True)


# cleaning and working on the dependent variable

# ranking the sales_performance column
sales_performance_rank = ['Sales decrease', 'No, noticeable change', 'Yes, a slight increase', 'Yes, a significant increase']
new_advert["sales_performance"] = pd.Categorical(new_advert["sales_performance"], categories=sales_performance_rank, ordered=True)

# ranking the positive_impact column
positive_impact_rank = ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']
new_advert["positive_impact"] = pd.Categorical(new_advert["positive_impact"], categories=positive_impact_rank, ordered=True)

# ranking the social_vs_sales column
social_vs_sales_rank = ['No noticeable impact', 'Sometimes, but not always', 'Yes, high engagement leads to more sales']
new_advert["social_vs_sales"] = pd.Categorical(new_advert["social_vs_sales"], categories=social_vs_sales_rank, ordered=True)

# the dependent varible sales_score
new_advert['sales_score'] = new_advert["positive_impact"].cat.codes + new_advert["social_vs_sales"].cat.codes + new_advert["sales_performance"].cat.codes

# my new dataframe for analysis
new_advert.drop(columns=['social_media', 'type', 'sales_performance', 'positive_impact', 'social_vs_sales'], inplace=True)


# convert to csv file for analysis
new_advert.to_csv("data/clean_advert.csv")

print("Execution successful!! File saved as clean_advert.csv in data folder.")
