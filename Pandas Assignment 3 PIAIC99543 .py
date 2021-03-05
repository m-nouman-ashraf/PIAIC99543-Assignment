#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob


# # Part 1
# 

# HOW TO CLEAN DATA WITH PYTHON
# Cleaning US Census Data
# You just got hired as a Data Analyst at the Census Bureau, which collects census data and creates interesting visualizations and insights from it.
# The person who had your job before you left you all the data they had for the most recent census. It is in multiple csv files. They didn’t use pandas, they would just look through these csv files manually whenever they wanted to find something. Sometimes they would copy and paste certain numbers into Excel to make charts.
# The thought of it makes you shiver. This is not scalable or repeatable.
# Your boss wants you to make some scatterplots and histograms by the end of the day. Can you get this data into pandas and into reasonable shape so that you can make these histograms?
# 
# Inspect the Data!
# 1.The first visualization your boss wants you to make is a scatterplot that shows average income in a state vs proportion of women in that state.
# Open some of the census csv files in the navigator. How are they named? What kind of information do they hold? Will they help us make this graph?
# 
# 2.It will be easier to inspect this data once we have it in a DataFrame. You can’t even call .head() on these csvs! How are you supposed to read them?
# Using glob, loop through the census files available and load them into DataFrames. Then, concatenate all of those DataFrames together into one DataFrame, called something like us_census.
# 
# 
# 3.Look at the .columns and the .dtypes of the us_census DataFrame. Are those datatypes going to hinder you as you try to make histograms?
# 
# 4.Look at the .head() of the DataFrame so that you can understand why some of these dtypes are objects instead of integers or floats.
# Start to make a plan for how to convert these columns into the right types for manipulation.
# Regex to the Rescue
# 5.Use regex to turn the Income column into a format that is ready for conversion into a numerical type.
# 
# 6.Look at the GenderPop column. We are going to want to separate this into two columns, the Men column, and the Women column.
# Split the column into those two new columns using str.split and separating out those results.
# 
# 7.Convert both of the columns into numerical datatypes.
# There is still an M or an F character in each entry! We should remove those before we convert.
# 
# 8.Now you should have the columns you need to make the graph and make sure your boss does not slam a ruler angrily on your desk because you’ve wasted your whole day cleaning your data with no results to show!
# Use matplotlib to make a scatterplot!
# plt.scatter(the_women_column, the_income_column) 
# Remember to call plt.show() to see the graph!
# 
# 9.Did you get an error? These monstrous csv files probably have nan values in them! Print out your column with the number of women per state to see.
# We can fill in those nans by using pandas’ .fillna() function.
# You have the TotalPop per state, and you have the Men per state. As an estimate for the nan values in the Women column, you could use the TotalPop of that state minus the Men for that state.
# Print out the Women column after filling the nan values to see if it worked!
# 
# 10.We forgot to check for duplicates! Use .duplicated() on your census DataFrame to see if we have duplicate rows in there.
# 
# 11.Drop those duplicates using the .drop_duplicates() function.
# 
# 12.Make the scatterplot again. Now, it should be perfect! Your job is secure, for now.Histograms of Races
# 
# 13.Now, your boss wants you to make a bunch of histograms out of the race data that you have. Look at the .columns again to see what the race categories are.
# 
# 14.Try to make a histogram for each one!
# You will have to get the columns into numerical format, and those percentage signs will have to go.
# Don’t forget to fill the nan values with something that makes sense! You probably dropped the duplicate rows when making your last graph, but it couldn’t hurt to check for duplicates again.
# Get Creative
# 
# 15.Phew. You’ve definitely impressed your boss on your first day of work.
# But is there a way you really convey the power of pandas and Python over the drudgery of csv and Excel?
# Try to make some more interesting graphs to show your boss, and the world! You may need to clean the data even more to do it, or the cleaning you have already done may give you the ease of manipulation you’ve been searching for

# In[6]:


path = r'C:\Users\HP\Desktop\Assignment'
fullfilename = glob.glob(path + "/states*.csv")

data = []
for filename in fullfilename:
    df = pd.read_csv(filename, index_col=None, header=0)
    data.append(df)

us_census = pd.concat(data, axis=0, ignore_index=True)
us_census


# In[48]:


us_census.head(10)


# In[49]:


us_census.drop(columns =["Unnamed: 0"], inplace = True)
us_census.columns


# In[50]:


us_census.dtypes


# # Income column to convert

# In[51]:


us_census["Income"] = us_census["Income"].replace({'\$':''}, regex=True)


# In[52]:


us_census["Income"] = pd.to_numeric(us_census["Income"])


# In[53]:


us_census.head(10)


# # Spliting Gender column

# In[54]:


GenderPop = us_census["GenderPop"].str.split("_",n=-1,expand=True)

us_census["Male"]=GenderPop[0]
us_census["Female"]=GenderPop[1]

us_census.drop(columns =["GenderPop"], inplace = True)


# In[55]:


us_census["Male"] = us_census["Male"].replace(to_replace='M',value='',regex=True)
us_census["Female"] = us_census["Female"].replace(to_replace='F',value='',regex=True)


# In[56]:


us_census["Male"] = pd.to_numeric(us_census["Male"])
us_census["Female"] = pd.to_numeric(us_census["Female"])
us_census["TotalPop"] = pd.to_numeric(us_census["TotalPop"])


# In[57]:


us_census.head(5)


# # Putting NAN Value

# In[58]:


us_census["Female"]=us_census["Female"].fillna(us_census["TotalPop"]-us_census["Male"])


# # Cheaking Duplicate

# In[59]:


isDuplicate = us_census[us_census.duplicated(keep=False)]
isDuplicate


# # Removing Duplicates:

# In[60]:


us_census = us_census.drop_duplicates()
us_census.shape


# # Scatter Plot:

# In[63]:


plt.scatter(us_census["Female"], us_census["Income"])
plt.title(" Average Income v/s Proportion of Women in a State")
plt.xlabel("Women")
plt.ylabel("Income ($)")
plt.show()


# # Histogram of Races

# removing % from columns

# In[65]:


columns = ["Hispanic", "White", "Black", "Native", "Asian", "Pacific"]
us_census[columns] = us_census[columns].replace({'%':''}, regex=True)


# In[67]:


us_census.head(10)


# # converting to Numeric Data

# In[70]:


us_census["Hispanic"] = pd.to_numeric(us_census["Hispanic"])
us_census["White"] = pd.to_numeric(us_census["White"])
us_census["Black"] = pd.to_numeric(us_census["Black"])
us_census["Native"] = pd.to_numeric(us_census["Native"])
us_census["Asian"] = pd.to_numeric(us_census["Asian"])
us_census["Pacific"] = pd.to_numeric(us_census["Pacific"])


# In[71]:


us_census.head(20)


# # check Duplicates:

# In[72]:


isDuplicate = us_census[us_census.duplicated(keep=False)]
isDuplicate


# In[73]:


us_census = us_census.drop_duplicates()
us_census.shape


# # Histogram:

# In[74]:


a = us_census.hist(column= "Hispanic","Native")


# In[75]:


a = us_census.hist(column= "Hispanic")


# In[76]:


c = us_census.hist(column= "Black")


# In[77]:


b = us_census.hist(column= "White")


# In[78]:


d = us_census.hist(column= "Native")


# In[79]:


e = us_census.hist(column= "Asian")


# In[89]:


fig, ax = plt.subplots(figsize=(8, 8))
ax.barh(us_census["State"], us_census["TotalPop"], color=(1,1,1,1), edgecolor = "green")


# In[88]:


fig, ax = plt.subplots(figsize=(12, 12))
ax.barh(us_census["State"], us_census["Income"], color=['pink'], edgecolor = 'black')


# # Scatter Plots:

# In[90]:


plt.scatter(us_census["TotalPop"], us_census["Income"])
plt.title(" Average Income v/s People in a State")
plt.xlabel("Population")
plt.ylabel("Income ($)")
plt.show()


# # Part 2

# LEARN DATA ANALYSIS WITH PANDAS
# Petal Power Inventory
# You’re the lead data analyst for a chain of gardening stores called Petal Power. Help them analyze their inventory!
# 
# 
# Answer Customer Emails
# 1.
# Data for all of the locations of Petal Power is in the file inventory.csv. Load the data into a DataFrame called inventory.
# 
# 2.
# Inspect the first 10 rows of inventory.
# 
# 3.
# The first 10 rows represent data from your Staten Island location. Select these rows and save them to staten_island.
# 
# 4.
# A customer just emailed you asking what products are sold at your Staten Island location. Select the column product_description from staten_island and save it to the variable product_request.
# 
# 5.
# Another customer emails to ask what types of seeds are sold at the Brooklyn location.
# 
# Select all rows where location is equal to Brooklyn and product_type is equal to seeds and save them to the variable seed_request
# 
# 
# 
# Inventory
# 6.
# Add a column to inventory called in_stock which is True if quantity is greater than 0 and False if quantity equals 0.
# 
# 7.
# Petal Power wants to know how valuable their current inventory is.
# 
# Create a column called total_value that is equal to price multiplied by quantity.
# 
# 8.
# The Marketing department wants a complete description of each product for their catalog.
# 
# The following lambda function combines product_type and product_description into a single string:
# 
# combine_lambda = lambda row: \
#     '{} - {}'.format(row.product_type,
#                      row.product_description)
# Paste this function into script.py.
# 
# 9.
# Using combine_lambda, create a new column in inventory called full_description that has the complete description of each product.

# In[5]:


inventory=pd.read_csv(r'C:\Users\HP\Desktop\Assignment\inventory.csv')
inventory


# In[94]:


inventory.head(10)


# In[103]:


staten_island = inventory.head(10)
product_request = inventory[inventory['location'] == "Staten Island"]
product_request


# In[98]:


inventory.dtypes


# In[119]:


seed_request=inventory[(inventory["location"] == "Brooklyn") & (inventory["product_type"] == "seeds")]
seed_request


# In[111]:


inventory['instock']=inventory['quantity'] >0


# In[112]:


inventory


# In[114]:


inventory['Total_price']=inventory['quantity']*inventory['price']
inventory


# In[115]:


combine_lambda = lambda row:'{} - {}'.format(row.product_type,row.product_description)
combine_lambda


# In[117]:


inventory['Full description']=inventory.apply(combine_lambda, axis=1)
inventory


# In[ ]:




