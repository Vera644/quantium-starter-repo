import pandas as pd


sales_0 = pd.read_csv('daily_sales_data_0.csv')
sales_1 = pd.read_csv('daily_sales_data_1.csv')
sales_2 = pd.read_csv('daily_sales_data_2.csv')

column_names = list(sales_0)

print(column_names)

sales_merged = pd.concat([sales_0,sales_1,sales_2], ignore_index=True)

filtered_df = sales_merged[sales_merged['product']=='pink morsel']

filtered_df['price'] = filtered_df['price'].str.replace('$', '')
filtered_df['price'] = pd.to_numeric(filtered_df['price'], downcast='integer', errors='coerce')

print(filtered_df.head(10))
print(filtered_df['price'].dtype)
filtered_df['sales'] = filtered_df['price'] * filtered_df['quantity']

filtered_df.drop(columns=["product"], axis=1, inplace=True)
filtered_df.drop(columns=["quantity"], axis=1, inplace=True)
filtered_df.drop(columns=["price"], axis=1, inplace=True)
print(filtered_df.head(10))
