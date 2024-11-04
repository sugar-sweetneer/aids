#Kaggle Dataset: https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers/data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_path = 'bank_churn.csv'
df = pd.read_csv(file_path)

print(df.head())
df = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'])
print(f"Shape of the dataset: {df.shape}")
print(df.describe())

print("\nMissing values in each column:")
print(df.isnull().sum()a)

# Bubble Plot
plt.figure(figsize=(12, 8))
plt.scatter(df['Balance'], df['Age'], s=df['EstimatedSalary']/1000, alpha=0.5, c=df['CreditScore'], cmap='coolwarm')
plt.colorbar(label='CreditScore')
plt.xlabel('Balance')
plt.ylabel('Age')
plt.title('Bubble Plot of Balance vs Age (Size by Estimated Salary, Color by CreditScore)')
plt.show()

features = ['Age', 'Tenure', 'EstimatedSalary']
fig, axes = plt.subplots(nrows=len(features), ncols=len(features), figsize=(12, 12))
for i in range(len(features)):
    for j in range(len(features)):
        if i == j:
            axes[i, j].hist(df[features[i]], bins=20, color='grey', alpha=0.7)
        else:
            axes[i, j].scatter(df[features[j]], df[features[i]], alpha=0.5)
        if i == len(features) - 1:
            axes[i, j].set_xlabel(features[j])
        if j == 0:
            axes[i, j].set_ylabel(features[i])

plt.tight_layout()
plt.show()


variables = ['CreditScore', 'Tenure', 'EstimatedSalary']

fig, axes = plt.subplots(len(variables), len(variables), figsize=(12, 12))

for i in range(len(variables)):
    for j in range(len(variables)):
        if i == j:
            axes[i, j].hist(df[variables[i]], bins=20, color='grey', alpha=0.7)
            axes[i, j].set_ylabel(variables[i])
        else:
            axes[i, j].scatter(df[variables[j]], df[variables[i]], alpha=0.5)
            if i == len(variables) - 1:
                axes[i, j].set_xlabel(variables[j])
            if j == 0:
                axes[i, j].set_ylabel(variables[i])

plt.tight_layout()
plt.show()


# 3D Scatter Plot
x = df['CreditScore']
y = df['EstimatedSalary']
z = df['Age']
geographies = df['Geography'].unique()


fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

for geography in geographies:
    subset = df[df['Geography'] == geography]
    ax.scatter(subset['CreditScore'], subset['EstimatedSalary'], subset['Age'], label=geography, alpha=0.7)

ax.set_xlabel('CreditScore')
ax.set_ylabel('EstimatedSalary')
ax.set_zlabel('Age')
ax.set_title('3D Scatter Plot of CreditScore, EstimatedSalary, and Age by Geography')
ax.legend(title='Geography')

plt.show()


# 3D Surface Plot
x = df['NumOfProducts']
y = df['HasCrCard']
z = df['Balance']

x_unique = np.sort(df['NumOfProducts'].unique())
y_unique = np.sort(df['HasCrCard'].unique())
X, Y = np.meshgrid(x_unique, y_unique)

Z = np.zeros_like(X, dtype=float)
for i in range(len(x_unique)):
    for j in range(len(y_unique)):
        mask = (df['NumOfProducts'] == x_unique[i]) & (df['HasCrCard'] == y_unique[j])
        Z[j, i] = df.loc[mask, 'Balance'].mean() if mask.sum() > 0 else np.nan

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

surface = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

ax.set_xlabel('NumOfProducts')
ax.set_ylabel('HasCrCard')
ax.set_zlabel('Balance')
ax.set_title('3D Surface Plot of Balance vs NumOfProducts and HasCrCard')

fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)

plt.show()

# Hexabin Plot
x = df['Point Earned']
y = df['EstimatedSalary']
size = df['NumOfProducts'] 

plt.figure(figsize=(12, 8))
hb = plt.hexbin(x, y, gridsize=30, cmap='Blues', reduce_C_function=np.mean, alpha=0.7)

cb = plt.colorbar(hb, label='Average Point Earned')
cb.set_label('Average Point Earned')

plt.xlabel('Point Earned')
plt.ylabel('EstimatedSalary')
plt.title('Hexbin Plot of Point Earned vs Estimated Salary')

plt.show()


# Grouped Bar Plot
summary = df.groupby(['Exited', 'Complain'])['Balance'].agg(['mean', 'std']).reset_index()

fig, ax = plt.subplots(figsize=(12, 8))

for complain in df['Complain'].unique():
    subset = summary[summary['Complain'] == complain]
    bar_width = 0.35
    x = np.arange(len(subset))
    
    bars = ax.bar(x + (0.5 if complain == df['Complain'].unique()[1] else -0.5) * bar_width,
                  subset['mean'],
                  bar_width,
                  yerr=subset['std'],
                  capsize=5,
                  label=f'Complain {complain}',
                  alpha=0.7)

ax.set_xlabel('Exited')
ax.set_ylabel('Average Balance')
ax.set_title('Grouped Bar Plot of Average Balance by Exit Status and Complaint')
ax.set_xticks(x)
ax.set_xticklabels(summary['Exited'].unique())
ax.legend(title='Complain')

plt.show()