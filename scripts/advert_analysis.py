# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")


# Load the dataset
advert_df = pd.read_csv("data/clean_advert.csv", index_col=[0])

# Exploratory data analysis
print(advert_df.info())

# Visualize the distribution of ads per category using a count plot
plt.figure(figsize=(10, 6))
sns.countplot(x="categories", data=advert_df, order=advert_df["categories"].value_counts().index, stat="percent")
plt.title("Number of Ads per Category")
plt.xlabel("Category")
plt.ylabel("Number of Ads")
plt.savefig("images/number_of_ads_per_category")

# Display the count of ads per category
advert_df["categories"].value_counts()


# Calculate the mean presence of ads on different social media platforms per category
advert_df.groupby("categories")[["Facebook", "Instagram", "Twitter", "LinkedIn", "WhatsApp", "TikTok", "Telegram", "Snapchat"]].mean()


# Visualize the mean presence of ads on different social media platforms per category
# plot new_df.groupby("categories").mean()
advert_df.groupby("categories")[["Facebook", "Instagram", "Twitter", "LinkedIn", "WhatsApp", 
                                  "TikTok", "Telegram", "Snapchat"]].mean().plot(kind='bar', figsize=(10, 6))
plt.title('Mean Advertising Platform Usage by Category')
plt.xlabel('Product/Service Category')
plt.ylabel('Mean Number of Platforms Used')
plt.xticks(rotation=20, ha='right')
plt.legend(title='Platform')
plt.tight_layout()
plt.savefig("images/catergory_by_media.png")


# Create subplots for each social media platform
cats = ['Facebook', 'Instagram', 'LinkedIn', 'Snapchat', 'Telegram', 'TikTok', 'Twitter', 'WhatsApp']

# Determine the number of rows and columns for the subplots
n_cols = 2
n_rows = (len(cats) + n_cols - 1) // n_cols

# Create a figure and axes for the subplots
fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, n_rows * 5))
axes = axes.flatten() # Flatten the 2D array of axes for easy iteration

for i, cat in enumerate(cats):
    sns.barplot(x="categories", y=cat, data=advert_df.groupby("categories")[["Facebook", "Instagram", "Twitter", "LinkedIn", "WhatsApp", 
                                                                          "TikTok", "Telegram", "Snapchat"]].mean().reset_index(), ax=axes[i])
    axes[i].set_title(f'Mean Usage for {cat}')
    axes[i].set_xlabel('Commodities')
    axes[i].set_ylabel(f'Mean Usage ({cat})')
    axes[i].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig("images/catergory_by_media_type.png")


# Regression Analysis
# Import necessary libraries for regression 
from sklearn.linear_model import LinearRegression       # Prepare data for regression analysis

# Define a function to perform linear regression
def regression_linear_model(df):
    X = df.drop(columns=["categories", "sales_score"]).values
    y = df[["sales_score"]].values
    model = LinearRegression(positive=True, fit_intercept=False)
    model.fit(X, y)
    return model.coef_


# Regression model for Clothing & Apparel
clothing_df = advert_df[advert_df["categories"] == "Clothing & Apparel"]
clothing_coef = regression_linear_model(clothing_df)

# Display the coefficients with corresponding feature names
print("Clothing & Apparel Coefficients:")
for i, col in enumerate(clothing_df.drop(columns=["categories", "sales_score"]).columns):
    print(f"{col}: \t {clothing_coef[0][i]:.3f}")


# Write the coefficients to a text file
with open("docs/reports.txt", "w") as f:
    f.write("Clothing & Apparel Coefficients: \n")
    for i, col in enumerate(clothing_df.drop(columns=["categories", "sales_score"]).columns):
        f.write(f"{col}: \t {clothing_coef[0][i]:.3f}\n")



# Regression model for Food & Beverages 
food_df = advert_df[advert_df["categories"] == "Food & Beverages"]
food_coef = regression_linear_model(food_df)
print("Food & Beverages Coefficients:")
for i, col in enumerate(food_df.drop(columns=["categories", "sales_score"]).columns):
    print(f"{col}: \t {food_coef[0][i]:.3f}")

# Append the coefficients to the text file
with open("docs/reports.txt", "a") as f:
    f.write("\nFood & Beverages Coefficients: \n")
    for i, col in enumerate(food_df.drop(columns=["categories", "sales_score"]).columns):
        f.write(f"{col}: \t {food_coef[0][i]:.3f}\n")


# Regression model for Home Appliances
home_df = advert_df[advert_df["categories"] == "Home Appliances"]
home_coef = regression_linear_model(home_df)
print("Home Appliances Coefficients:")
for i, col in enumerate(home_df.drop(columns=["categories", "sales_score"]).columns):
    print(f"{col}: \t {home_coef[0][i]:.3f}")

# Append the coefficients to the text file
with open("docs/reports.txt", "a") as f:
    f.write("\nHome Appliances Coefficients: \n")
    for i, col in enumerate(home_df.drop(columns=["categories", "sales_score"]).columns):
        f.write(f"{col}: \t {home_coef[0][i]:.3f}\n")



# Modelling with gradio 

# import gradio for building interactive web apps
import gradio as gr

# Function to convert "Yes"/"No" input to binary
def Options(inpt):
    if inpt == "Yes":
        return 1
    else:
        return 0     

# Function to interpret the sales score
def result(val):
    if val <= 4:
        return "Low impact on sales"
    elif val <= 7:
        return "Moderate impact on sales"
    else:
        return "High impact on sales"


# Function to predict sales score based on category and social media usage
# Define the prediction function
def sales_score_prediction(typee, fb, ig, tw, lin, wb, tik, tg, sc):
    social_media_used = np.array([Options(fb), Options(ig), Options(tw), 
                                  Options(lin), Options(wb), Options(tik), Options(tg), Options(sc)])
    coef = regression_linear_model(advert_df[advert_df["categories"] == typee])
   
    # Make prediction based on category
    if typee == "Clothing & Apparel":
        return result(np.dot(coef, social_media_used)[0])
    elif typee == "Food & Beverages":
        return result(np.dot(coef, social_media_used)[0])
    elif typee == "Home Appliances":
        return result(np.dot(coef, social_media_used)[0])

# Define the Gradio interface
iSales = gr.Interface(
    fn=sales_score_prediction,
    # Define the input components for the Gradio interface
    inputs=[gr.Dropdown(label="Your Message", choices=["Clothing & Apparel", "Food & Beverages", "Home Appliances"]), 
            gr.Dropdown(label="Do you use Facebook for your advertisement?", choices=["Yes", "No"]), 
            gr.Dropdown(label="Do you use Instagram for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use Twitter/X for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use LinkedIn for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use WhatsApp for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use TikTok for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use Telegram for your advertisement?", choices=["Yes", "No"]),
           gr.Dropdown(label="Do you use SnapChat for your advertisement?", choices=["Yes", "No"])],
    # Define the output component for the Gradio interface
    outputs=gr.Text(label="Report"),
    title="Sales Prediction",
    description="It gives sales prediction with respect to types of social media use for advertisement in different categories of products/services.",
    theme="compact"
)

# Launch the Gradio app
iSales.launch()

