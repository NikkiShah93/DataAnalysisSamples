import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import datetime
style.use("ggplot")

### First, we want to read all of the csv files in the folder
### and concat them in a single file

dataset = pd.DataFrame()
directory = './Sales_Data/'
for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
        file_location = os.path.join(directory, filename)
        dataset = pd.concat([dataset, pd.read_csv(file_location, parse_dates=['Order Date'])])
dataset.replace('Order Date', np.nan, inplace = True)
dataset.dropna(inplace = True)

### which month has the highest sale?

def sale(data):
    if data[0] is not np.nan and data[0].lower().find('quantity') == -1:
        return int(data[0])*float(data[1])
    else:
        return 0
    

dataset_month = dataset.copy()
dataset_month['Month'] = [x.split('/')[0] if type(x)==str else x for x in dataset_month['Order Date'].values]
dataset_month['Sale'] = dataset_month[['Quantity Ordered','Price Each']].apply(sale, axis = 1)
dataset_month_total_sale = dataset_month.groupby('Month')['Sale'].agg({'Total Sale':sum}).reset_index().sort_values('Total Sale', ascending = False)
print(dataset_month_total_sale.head(5))

## storing month names in a list for plotting

month_name = [datetime.datetime.strptime(x, "%m").strftime("%b") for x in dataset_month_total_sale['Month'].values]

## showing the result in a bar graph could be useful

plt.bar(dataset_month_total_sale['Month'].astype(int).tolist(), dataset_month_total_sale['Total Sale'].tolist())
plt.xticks(dataset_month_total_sale['Month'].astype(int).tolist(), month_name, rotation=90)
plt.title('Total Sale by Month')
plt.xlabel('Month of Year')
plt.ylabel('Total Sale')
plt.grid(True)
plt.show()

## we could plot the same data using seaborn too, which is slightly easier
## since seaborn works better with DataFrames

sns.set(style="darkgrid")
sale_plot = sns.barplot(x= 'Month', y = 'Total Sale', data=dataset_month_total_sale)
sale_plot.set_xticks(range(len(dataset_month_total_sale)))
sale_plot.set_xticklabels(month_name)
plt.title('Total Sale by Month')
plt.xlabel('Month')
plt.ylabel('Total Sale')
plt.show()

## now we know that we had the highest sale in December

## Let's check what item has been sold the most?

dataset_item_most_sold = dataset.groupby('Product')['Quantity Ordered'].agg({'Total Count':'count'}).reset_index().sort_values('Total Count', ascending = False)
print(dataset_item_most_sold.head(5))

## seems like the "USB-C Charging Cable" has been sold the most in 2019

## Now, let's see what zipcodes have bought the most products?

dataset_zipcode = dataset.copy()
dataset_zipcode['Zipcode'] = [x.rsplit(' ', 1)[1] if type(x)==str else x for x in dataset_zipcode['Purchase Address'].values]
dataset_zipcode['Sale'] = dataset_zipcode[['Quantity Ordered','Price Each']].apply(sale, axis = 1)
dataset_zipcode_sale = dataset_zipcode.groupby('Zipcode')['Sale'].agg({'Total Sale':sum}).reset_index().sort_values('Total Sale', ascending = False)
print(dataset_zipcode_sale.head(5))

## zipcode 94016 has the highest sale