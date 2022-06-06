import pandas as pd
import os

#merging all the monthly sales data into a single file

directory_csv_files = r"C:\Users\User\PycharmProjects\Sales data analysis\Sales_Data\{}"
files = [file for file in os.listdir(r'C:\Users\User\PycharmProjects\Sales data analysis\Sales_Data')]
all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(directory_csv_files.format(file))
    all_months_data = pd.concat([all_months_data, df])

print(all_months_data)