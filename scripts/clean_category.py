# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# read the dataset
df = pd.read_csv("data/responses.csv")

# display the first few rows of the dataframe
print(df.head())

# rename columns for easier access
df.rename(columns={'What type of products or services does your business offer?': 'type',
                  'Which social media platforms do you advertise on? (Select all that apply)': "social_media",
                  'Have you noticed any changes in sales performance since using social media?': "sales_performance",
                  'Do you believe social media has a positive impact on your sales performance?': "positive_impact",
                  'Have you noticed any correlation between social media engagement and sales performance?': "social_vs_sales"}, inplace=True)

# clean the 'type' column by stripping leading/trailing whitespace
df["type"] = df["type"].str.strip()
df["type"].unique()

# categorize the 'type' column into broader categories
home = ['Electronics & Gadgets', 'Accessories', 'Kitchen utensils', 'Construction', 'Cooking gas', 'Electrical', 'Photography',
         'Internet, designs', 'Household items', 'Home essentials', 'Graphics','Tech', 'Science Lab/Equipments']
cloth = ['Clothing & Apparel', 'Barber', 'Cosmetics and deodorant', 'Crochet wears', 'Drycleaning', 'Perfume', 'Finance', 'Fashion designer',
        'Banking system', 'Makeup artist', 'Frame, Throw Pillow, Mug, Magic Mug, and other gift items for birthday surprises', 'Haircut',
        'Catering and Decoration', "Hair", 'Loc’s and carve']
food = ["Food & Beverages", 'Chemist store', 'Drugs', 'Farming  and poultry',  'Educational', 'Petty trade', 'Educational institute',
        'Clothing and food', 'Snacks']

# create a new column 'categories' based on the 'type' column
df.loc[:, "categories"] = np.nan
for i, types in enumerate(df["type"]):
    if types in home:
        df.loc[i, "categories"] = 'Home Appliances'
    elif types in cloth:
        df.loc[i, "categories"] = 'Clothing & Apparel'
    elif types in food:
        df.loc[i, "categories"] = 'Food & Beverages'
    else:
        df.loc[i, "categories"] = np.nan

# display the unique values in the 'categories' column
print(df["categories"].unique())

with open("docs/cleaned_category.txt", "w") as f:
    f.write("Cleaned Categories:\n")
    for category in df["categories"].unique():
        f.write(f"- {category}\n")


# Count the number of businesses using social media for advertising
df['Do you use social media platforms for advertising?'].value_counts() 
with open("docs/cleaned_category.txt", "a") as f:
    f.write("\n\nSocial Media Advertising Usage:\n")
    f.write(df['Do you use social media platforms for advertising?'].value_counts().to_string())

# Filter the dataframe to include only those who use social media for advertising
df1 = df[df['Do you use social media platforms for advertising?']=="Yes"]

# Select relevant columns for analysis
advert = df1[["type", "social_media", "categories", "sales_performance", "positive_impact", "social_vs_sales"]]
advert = advert.copy()

# Drop rows with missing values and reset index
advert.dropna(inplace=True)
advert.reset_index(drop=True, inplace=True)

# Display the count of each category
advert["categories"].value_counts(dropna=False)

with open("docs/cleaned_category.txt", "a") as f:
    f.write("\n\nCategory Counts After Cleaning:\n")
    f.write(advert["categories"].value_counts(dropna=False).to_string())


# Save the cleaned dataframe to a new CSV file
advert.to_csv("data/advert_categories.csv") 

# End of clean_category.py
