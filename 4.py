import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv('/content/drive/MyDrive/AIDS/Cost_of_Living_Index_by_Country_2024.csv')
sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))
top_10_countries = dataset.nlargest(10, 'Cost of Living Index')
sns.barplot(x='Cost of Living Index', y='Country', data=top_10_countries, palette='viridis')
plt.title('Top 10 Countries by Cost of Living Index')
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x='Cost of Living Index', y='Rent Index', data=dataset, hue='Country', palette='coolwarm', legend=False)
plt.title('Rent Index vs. Cost of Living Index')
plt.show()

plt.figure(figsize=(10, 6))
correlation_matrix = dataset[['Cost of Living Index', 'Rent Index', 'Cost of Living Plus Rent Index', 'Groceries Index', 'Restaurant Price Index', 'Local Purchasing Power Index']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Various Indexes')
plt.show()

sns.pairplot(dataset[['Cost of Living Index', 'Rent Index', 'Cost of Living Plus Rent Index', 'Groceries Index', 'Restaurant Price Index', 'Local Purchasing Power Index']])
plt.title('Pairplot of Various Indexes')
plt.show()

sns.lmplot(x='Rent Index', y='Cost of Living Index', hue='Restaurant Price Index', data=dataset, palette='coolwarm', height=6, aspect=1.5)
plt.title('Regression of Cost of Living Index on Rent and Restaurant Price Index')
plt.show()
