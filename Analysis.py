import matplotlib.pyplot as plt
import pandas as pd
import os
import mplcursors
import matplotlib
from collections import Counter
from itertools import combinations

#merging all the monthly sales data into a single file
import pylab as pl

directory_csv_files = r"C:\Users\User\PycharmProjects\Sales data analysis\Sales_data_analysis\Sales_Data\{}"
files = [file for file in os.listdir(r"C:\Users\User\PycharmProjects\Sales data analysis\Sales_data_analysis\Sales_Data")]
all_months_data = pd.DataFrame()

#combining all the sales data into single file, so that all the data can be compared to each other.
for file in files:
    df = pd.read_csv(directory_csv_files.format(file))
    all_months_data = pd.concat([all_months_data, df])

#cleaning data, to deal with missing values
all_data = all_months_data.dropna(how= 'all')

#we have data of few months in the form of string values(Order Date)
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

#some of the numerical data is in the string format, so here we gonna convert them to int using pandas
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#adding an extra column of month, so that data seggregation is easy.
all_data['Month'] = all_data['Order Date'].str[0:2].astype('int32')

#detreming the month which has best sales
#adding an extra row with total order values
all_data['Total sales'] = all_data['Quantity Ordered']*all_data['Price Each']

#converting the data frame into a CSV file
all_data.to_csv('all_data.csv', index = False)


#Determining the months with highest sales
best_sales = all_data.groupby('Month').sum()

#####Visualisation with Bar chart
months = range(1,13)
month_names = []
month_names = ['Dummy', 'January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

fig, ax = plt.subplots()
plt.bar(months, best_sales['Total sales'])
ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xticks(months)
plt.ylabel('Sales in millions($)')
plt.xlabel('Months')
plt.title('Sales report of the year')

#Exact Sales values will be availaible in the bar chart when the pointer hover overs the Bars

cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    sel.annotation.set(text=f"{month_names[round(x)]} :{round(height)}{'$'}",
                       position=(-10, -10), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height / 2)

plt.tight_layout()
plt.show()

#Which city have the highest sales
#For this analysis we need a column of city

all_data['City'] = all_data['Purchase Address'].apply(lambda x : x.split(',')[1] + (',') + x.split(',')[2].split(' ')[1])
best_sales_city = all_data.groupby('City').sum()

#Visulaisation with resptect to cities
fig, ax = plt.subplots()
cities = [city for city, df in all_data.groupby('City')]
plt.bar(cities, best_sales_city['Total sales'])
plt.xticks(cities,rotation=90, size = 5)
ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.ylabel('Sales in millions($)')
plt.xlabel('Cities')
plt.title('Sales report of the year')

ursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    sel.annotation.set(text=f"{cities[round(x)]} :{height}{'$'}",
                       position=(-10, -10), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height / 2)

plt.show()

#What time should the advertisements be displayed to increase the likelihood of the customer buying the product

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute


#Visualisation of number of orders placed in accordance with time using line chart
hours=[hour for hour,df in all_data.groupby('Hour')]
plt.title('Number of orders placed in accordance with time')
plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of products ordered')
plt.grid()
plt.show()


#What products are often sold together?
df= all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']= df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()

#converting the data frame into a CSV file
all_data.to_csv('all_data.csv', index = False)

count=Counter()
for row in df['Grouped']:
   row_list=row.split(',')
   count.update(Counter(combinations(row_list,2)))

print(count.most_common(10))


#Most ordered items and the probable reasons for their high sales.

items = all_data.groupby('Product')
quantity_of_ordered_items = items.sum()['Quantity Ordered']
items_list = [item for item, df in items]

prices = all_data.groupby('Product').mean()['Price Each']
fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(items_list,quantity_of_ordered_items)
ax2.plot(items_list,prices,'b-')
ax1.set_xlabel('Name of the Item')
ax2.set_ylabel('Price of the Item in dollars($)', color = 'blue')
ax1.set_ylabel('Quantity ordered')
ax1.set_xticklabels(items_list,rotation=90, size = 5)
plt.show()
