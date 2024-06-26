# -*- coding: utf-8 -*-
"""MSCI 402 Data Analytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17rENeeIqWNxtGCOXR9cMj02ikHINs5XL
"""

#we will also need to calculate the percentages

#what are we getting from the ML algorithm?
#basically, each answer to each question will have a
#result:

#we need to make the prediction of which eng program that they will end up in based on the data from the google form
#it is calculating the probability that you (the sample) should belong to each of the categories - then an ordered list is created

#what happens during the running of the visual novel?
#as they answer each question, there are 3 separate counts: MGMT, SYDE, SOFT, which are calculated / N to give the percentage that they are of each program
#we have N number of questions (between 10-12)
#result:

#the math: (x/3 - percentage of MGMT/SYDE/SOFt that chose that option) - out of 3 question options = % of 1 added towards total count / N
#the other math: (x/3) / 2 - out of the 2 options

#imports

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB

from google.colab import files
uploaded = files.upload()

import io

categorical_cols = ['Timestamp', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']
selected_cols = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']

import chardet
with open("MSCI402TestResponsesFINAL (1).csv", "rb") as f:
    encoding = chardet.detect(f.read())["encoding"]

df = pd.read_csv("MSCI402TestResponsesFINAL (1).csv", usecols = categorical_cols, encoding=encoding)

# setup inital column names and read dataset


df.columns = [c.replace(' ', '-') for c in df.columns]
df.columns = [c.replace(' ', '_') for c in df.columns]
categorical_cols = [c.replace(' ', '-') for c in categorical_cols]
categorical_cols = [c.replace(' ', '_') for c in categorical_cols]

print(df)

print(df.info())
print(df.head())

# Drop rows with missing values
df = df.dropna()

df.head()

data = df[selected_cols]
data.head()

data.info()

# Perform one-hot encoding
data_ONE = pd.get_dummies(data, columns=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10'])

target_mapping = {'Management Engineering': 0, 'Software Engineering': 1, 'Systems Design Engineering': 2}

data_ONE.head()

# Map the target variable to one-hot encoded values and maintain mapping to original values
data_ONE['Q11_encoded'] = data['Q11'].map(target_mapping)

# Separate features and target variable
X = data_ONE.drop(['Q11', 'Q11_encoded'], axis=1)
y = data_ONE['Q11_encoded']

# Reverse mapping for target variable
reverse_target_mapping = {value: key for key, value in target_mapping.items()}

#IN USE

# Create an empty DataFrame to store the results
results_df = pd.DataFrame()

# Iterate over each column (excluding the target column)
for column in X.columns:
    feature = X[[column]]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(feature, y, test_size=0.2, random_state=42)

    # Naive Bayes classifier
    nb_classifier = GaussianNB()
    nb_classifier.fit(X_train, y_train)

    # Get predicted probabilities for each class
    predicted_probabilities = nb_classifier.predict_proba(X_test)

    # Calculate the mean or median of the predicted probabilities
    mean_probabilities = predicted_probabilities.mean(axis=0)  # You can use .mean() or .median() here

    # Store the mean or median predicted probabilities in the DataFrame
    results_df[column] = mean_probabilities

# Export the DataFrame to a CSV file
results_df.to_csv('predicted_probabilities.csv', index=False)

# Create empty lists to store results
results_data = []

# Iterate over each column (excluding the target column)
for column in X.columns:
    feature = X[[column]]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(feature, y, test_size=0.2, random_state=42)

    # Naive Bayes classifier
    nb_classifier = GaussianNB()
    nb_classifier.fit(X_train, y_train)

    # Get unique class labels and their corresponding indices
    class_labels = nb_classifier.classes_

    # Make predictions
    y_pred = nb_classifier.predict(X_test)

    # Obtain predicted probabilities
    predicted_probabilities = nb_classifier.predict_proba(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy for {column}: {accuracy}")

    # Print out the actual, predicted values, and probabilities
    print(f"Predictions for {column}:")
    for actual, predicted, probabilities in zip(y_test, y_pred, predicted_probabilities):
        actual_label = reverse_target_mapping[actual]
        predicted_label = reverse_target_mapping[predicted]
        class_probabilities = {class_labels[i]: prob for i, prob in enumerate(probabilities)}
        print(f"Actual: {actual_label}, Predicted: {predicted_label}, Probabilities: {class_probabilities}")

    #trying to get csv of results
    # Store results in a dictionary
    result = {
        'Feature': column,
        'Accuracy': accuracy,
        'Predictions': [{'Actual': reverse_target_mapping[actual],
                         'Predicted': reverse_target_mapping[predicted],
                         'Probabilities': {class_labels[i]: prob for i, prob in enumerate(probabilities)}}
                        for actual, predicted, probabilities in zip(y_test, y_pred, predicted_probabilities)]
    }

    # Append result to results_data list
    results_data.append(result)

# Convert results_data to DataFrame
results_df = pd.DataFrame(results_data)

# Export results to CSV
results_df.to_csv('naive_bayes_results.csv', index=False)

# Iterate over each column (excluding the target column)
for column in X.columns:
    feature = X[[column]]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(feature, y, test_size=0.2, random_state=42)

    # Naive Bayes classifier
    nb_classifier = GaussianNB()
    nb_classifier.fit(X_train, y_train)

    # Get unique class labels and their corresponding indices
    class_labels = nb_classifier.classes_

    # Make predictions
    y_pred = nb_classifier.predict(X_test)

    # Obtain predicted probabilities
    predicted_probabilities = nb_classifier.predict_proba(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Print out the actual, predicted values, and probabilities
    print(f"Predictions for {column}:")
    for actual, predicted, probabilities in zip(y_test, y_pred, predicted_probabilities):
        actual_label = reverse_target_mapping[actual]
        predicted_label = reverse_target_mapping[predicted]
        print(f"Actual: {actual_label}, Predicted: {predicted_label}, Probabilities: {probabilities}")

# Separate features (answers to questions) and target variable
X = data.drop('Q11', axis=1)
y = data['Q11']

# Define the categories for each question
categories = [['a', 'b', 'c'], ['x', 'y', 'z']]

# One-hot encode the features
encoder = OneHotEncoder(categories=categories, sparse=False)
X_encoded = encoder.fit_transform(X)

# Label encode the target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train a Naive Bayes classifier
nb_classifier = GaussianNB()
nb_classifier.fit(X_encoded, y_encoded)

# Define a function to calculate probabilities for specific scenarios
def get_probabilities(df_row):
    # Create a DataFrame with the provided row for Q1 and a valid category for Q2
    df_row = pd.DataFrame([df_row], columns=['Q1', 'Q2'])

    # One-hot encode the input DataFrame row
    encoded_row = encoder.transform(df_row)

    # Predict probabilities
    probabilities = nb_classifier.predict_proba(encoded_row)[0]

    # Map probabilities to original answer labels
    mapped_probabilities = {}
    for class_label, probability in zip(nb_classifier.classes_, probabilities):
        mapped_probabilities[label_encoder.inverse_transform([class_label])[0]] = probability

    return mapped_probabilities

# Example usage:
# Get probabilities for the scenario where Q1 is 'a' only
probabilities_1a_only = get_probabilities(['a', 'x'])  # Provide a valid category for Q2, e.g., 'x'
print("Probabilities for Q1='a' only:")
print(probabilities_1a_only)

from sklearn.metrics import classification_report

# Combine y_test and y_pred to get all unique labels
combined_labels = np.concatenate((y_test, y_pred))

# Fit a new label encoder on the combined set of labels
new_encoder = LabelEncoder()
new_encoder.fit(combined_labels)

# Convert y_test and y_pred to numeric labels using the new encoder
y_test_encoded = new_encoder.transform(y_test)
y_pred_encoded = new_encoder.transform(y_pred)

# Define a mapping dictionary for original labels
original_label_mapping = {idx: label for idx, label in enumerate(original_labels)}
#for idx, label in original_label_mapping.items():
    #print(f"Index: {idx}, Label: {label}")

# Compute classification report
report = classification_report(y_test_encoded, y_pred_encoded, output_dict=True)

# Print classification report for each original label
for label_idx, original_label in original_label_mapping.items():
    try:
        report_entry = report[str(label_idx)]
        print(f"Classification Report for '{original_label}':")
        print(f"Precision: {report_entry['precision']}")
        print(f"Recall: {report_entry['recall']}")
        print(f"F1-score: {report_entry['f1-score']}")
        print(f"Support: {report_entry['support']}\n")
    except KeyError:
        print(f"No classification report available for '{original_label}'")