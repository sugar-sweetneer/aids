import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Coffee-Shop-Sales.csv')

print("Basic Information:")
print(df.info())

print("\nFirst Few Rows:")
print(df.head())

print("\nSummary Statistics:")
print(df.describe(include='all'))

print("\nMissing Values:")
print(df.isnull().sum())

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.time

df['total_sales'] = df['transaction_qty'] * df['unit_price']
plt.figure(figsize=(12, 6))
sns.barplot(x='store_location', y='total_sales', data=df, estimator=np.sum)
plt.title('Total Sales by Store Location')
plt.xlabel('Store Location')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

sales_by_product_store = df.groupby(['store_location', 'product_type'])['total_sales'].sum().unstack().fillna(0)
sales_by_product_store.plot(kind='bar', stacked=True, figsize=(14, 7), colormap='Paired')
plt.title('Stacked Bar Plot of Sales by Product Type and Store Location')
plt.xlabel('Store Location')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.legend(title='Product Type')
plt.grid(True)
plt.tight_layout()
plt.show()

pivot_table = df.pivot_table(values='total_sales', index='store_location', columns='product_category', aggfunc=np.sum, fill_value=0)
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='.2f')
plt.title('Total Sales Heatmap by Store Location and Product Category')
plt.xlabel('Product Category')
plt.ylabel('Store Location')
plt.tight_layout()
plt.show()

daily_sales = df.groupby('transaction_date')['total_sales'].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales['transaction_date'], daily_sales['total_sales'], marker='o')
plt.title('Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df['transaction_qty'], bins=30, color='skyblue', edgecolor='black')
plt.title('Histogram of Transaction Quantities')
plt.xlabel('Transaction Quantity')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

df['hour_of_day'] = df['transaction_time'].apply(lambda x: x.hour)
df['day_of_week'] = df['transaction_date'].dt.day_name()

pivot_table = df.pivot_table(values='total_sales', index='day_of_week', columns='hour_of_day', aggfunc=np.mean, fill_value=0)
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt='.1f', linewidths=0.5)
plt.title('Average Sales by Hour of Day and Day of Week')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 6))
sns.scatterplot(x='unit_price', y='transaction_qty', hue='product_category', data=df, palette='Set1', alpha=0.6)
plt.title('Unit Price vs. Transaction Quantity by Product Category')
plt.xlabel('Unit Price')
plt.ylabel('Transaction Quantity')
plt.legend(title='Product Category')
plt.grid(True)
plt.tight_layout()
plt.show()