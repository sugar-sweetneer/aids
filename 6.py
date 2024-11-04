import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score, roc_curve, roc_auc_score 

data = pd.read_csv("/content/drive/MyDrive/AIDS/titanic.csv")

print("First few rows of the dataset:")
print(data.head())
print("\nMissing values in the dataset:")
print(data.isnull().sum())

data['Embarked'] = data['Embarked'].astype(str)
most_frequent_embarked = data['Embarked'].mode()[0]
data['Embarked'].fillna(most_frequent_embarked, inplace=True)
print("\nAfter imputation:")
print(data[['Embarked']].head())
data.drop(columns=['Cabin'], inplace=True)
label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])
data['Embarked'] = label_encoder.fit_transform(data['Embarked'])
data.drop(columns=['Name', 'Ticket', 'PassengerId'], inplace=True)
print("\nCleaned DataFrame:")
print(data.head())

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Fare', y='Pclass', hue='Survived', data=data, palette='viridis', alpha=0.6)
plt.title('Survival by Fare and Pclass')
plt.xlabel('Fare')
plt.ylabel('Pclass')
plt.legend(title='Survived', labels=['Not Survived', 'Survived'])
plt.show()

plt.figure(figsize=(10, 8))
correlation_matrix = data[['Age', 'Fare', 'Pclass', 'Sex', 'Embarked', 'Survived']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Heatmap of Correlations')
plt.show()

plt.figure(figsize=(12, 10))
sns.pairplot(data, hue='Survived', vars=['Age', 'Fare', 'Pclass'], palette='viridis', diag_kind='kde')
plt.title('Pair Plot of Age, Fare, and Pclass')
plt.show()

X = data.drop(columns=['Survived'])
y = data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

dt_model = DecisionTreeClassifier()
nb_model = GaussianNB()
dt_model.fit(X_train, y_train)
nb_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)
nb_predictions = nb_model.predict(X_test)

dt_cm = confusion_matrix(y_test, dt_predictions)
nb_cm = confusion_matrix(y_test, nb_predictions)
def plot_confusion_matrix(cm, model_name, labels):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.show()
labels = ['Not Survived', 'Survived']
print("Decision Tree Confusion Matrix:")
plot_confusion_matrix(dt_cm, 'Decision Tree', labels)
print("Naive Bayes Confusion Matrix:")
plot_confusion_matrix(nb_cm, 'Naive Bayes', labels)

print("\nDecision Tree Classification Report:")
print(classification_report(y_test, dt_predictions))
print("\nNaive Bayes Classification Report:")
print(classification_report(y_test, nb_predictions))

def evaluate_model(y_test, y_pred, model_name):
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(f"{model_name} Evaluation:")
    print(f"Accuracy: {100 * accuracy:.2f}%")
    print(f"Precision: {100 * precision:.2f}%")
    print(f"Recall: {100 * recall:.2f}%")
    print(f"F1-Score: {100 * f1:.2f}%")
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [accuracy, precision, recall, f1]
    fig, ax = plt.subplots()
    ax.bar(metrics, [100 * v for v in values], width=0.5, color="purple")
    ax.set_title(model_name)
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values (%)')
    plt.show()
evaluate_model(y_test, dt_predictions, "Decision Tree")
evaluate_model(y_test, nb_predictions, "Naive Bayes")

dt_probabilities = dt_model.predict_proba(X_test)[:, 1]
nb_probabilities = nb_model.predict_proba(X_test)[:, 1]
dt_fpr, dt_tpr, _ = roc_curve(y_test, dt_probabilities)
nb_fpr, nb_tpr, _ = roc_curve(y_test, nb_probabilities)
dt_auc = roc_auc_score(y_test, dt_probabilities)
nb_auc = roc_auc_score(y_test, nb_probabilities)
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.plot(dt_fpr, dt_tpr, color='blue', label=f'Decision Tree (AUC = {dt_auc:.2f})')
plt.plot([0, 1], [0, 1], color='grey', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Decision Tree')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(nb_fpr, nb_tpr, color='green', label=f'Naive Bayes (AUC = {nb_auc:.2f})')
plt.plot([0, 1], [0, 1], color='grey', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Naive Bayes')
plt.legend()
plt.tight_layout()
plt.show()
print(f"Decision Tree AUC: {dt_auc:.2f}")
print(f"Naive Bayes AUC: {nb_auc:.2f}")

importances = dt_model.feature_importances_
features = X.columns
feature_importances = pd.DataFrame({'Feature': features, 'Importance': importances})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
print("\nFeature Importances:")
print(feature_importances)
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importances)
plt.title('Feature Importances')
plt.show()

def predict_with_decision_tree(model, input_data):
    return model.predict(input_data)
def predict_with_naive_bayes(model, input_data):
    return model.predict(input_data)
sample_values = np.array([[3, 22, 1, 0, 7.25, 0, 1],
                          [1, 38, 1, 0, 71.2833, 1, 1],
                          [3, 26, 0, 0, 7.925, 0, 0]])
sample_df = pd.DataFrame(sample_values, columns=X.columns)
dt_predictions = predict_with_decision_tree(dt_model, sample_df)
nb_predictions = predict_with_naive_bayes(nb_model, sample_df)
def explain_prediction(predictions):
    return ["Survived" if p == 1 else "Not Survived" for p in predictions]

print("Decision Tree Predictions (0 = Not Survived, 1 = Survived):", dt_predictions)
print("Naive Bayes Predictions (0 = Not Survived, 1 = Survived):", nb_predictions)
print("Decision Tree Predictions Explained:", explain_prediction(dt_predictions))
print("Naive Bayes Predictions Explained:", explain_prediction(nb_predictions))
