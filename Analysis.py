import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
import mplcursors

#merging all the monthly sales data into a single file
import pylab as pl

directory_csv_files = r"C:\Users\User\PycharmProjects\Sales data analysis\Sales_data_analysis\Sales_Data\{}"
files = [file for file in os.listdir(r"C:\Users\User\PycharmProjects\Sales data analysis\Sales_data_analysis\Sales_Data")]
all_months_data = pd.DataFrame()

#combining all the sales data into single file, so that all the data can be compared to each other.
for file in files:
    df = pd.read_csv(directory_csv_files.format(file))
    all_months_data = pd.concat([all_months_data, df])

#converting the data frame into a CSV file
all_months_data.to_csv('all_months_data.csv', index = False)

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

#Determining the months with highest sales
best_sales = all_data.groupby('Month').sum()

#####Visualisation with Bar chart
months = range(1,13)
month_names = []
month_names = ['Dummy', 'January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
highest_sale = int(best_sales['Total sales'].max())
sales = range(1000000,round(highest_sale)+ 1000000 , 1000000)

fig, ax = plt.subplots()
plt.bar(months, best_sales['Total sales'])
ax.ticklabel_format(style='plain')
plt.xticks(months)
plt.ylabel('Sales in millions($)')
pl.xlabel('Months')
plt.title('Sales report of the year')

cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
    sel.annotation.set(text=f"{  month_names[round(x)]} :{height}{'$'}",
                       position=(10, 0), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height / 2)
    print(x)
    #sel.annotation.get_bbox_patch().set(alpha=0.8)

plt.tight_layout()


plt.show()

