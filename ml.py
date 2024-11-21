import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

################################################### Cleaning and preprocessing data ###################################################

# Load dataset
file_path = 'weather_data/Weather Training Data.csv'
weather_data = pd.read_csv(file_path)

# Drop columns with excessive missing values
columns_to_drop = ['Evaporation', 'Sunshine', 'Cloud9am', 'Cloud3pm']
weather_data.drop(columns=columns_to_drop, inplace=True)

# Separate features and target variable
X = weather_data.drop(columns=['RainTomorrow', 'row ID'])
y = weather_data['RainTomorrow']

# Identify numerical and categorical columns
numerical_cols = X.select_dtypes(include=['float64']).columns
categorical_cols = X.select_dtypes(include=['object']).columns

# Preprocessing for numerical data: Impute missing values, then scale
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # Replace with 'median' if needed
    ('scaler', StandardScaler())  # Standardize numerical features
])

# Preprocessing for categorical data: Impute missing values, then encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute with mode
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # One-hot encoding
])

# Combine preprocessors in a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)

# Apply preprocessing
X_processed = preprocessor.fit_transform(X)

# Resample the dataset using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_processed, y)
print("Resampled Dataset Shape:", X_resampled.shape, y_resampled.shape)


# Print processed feature set shape
print("Processed Features Shape:", X_processed.shape)

################################################### Model Training ###################################################

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save feature means and preprocessing pipeline with the model
feature_means = X.select_dtypes(include=["number"]).mean().to_dict()  # Compute mean for each feature before preprocessing

# Save model, preprocessing pipeline, and feature means
model_data = {
    "model": model,
    "preprocessor": preprocessor,  # Save the preprocessing pipeline
    "feature_means": feature_means,  # Save feature means for default values
}
joblib.dump(model_data, "decision_tree_model_with_pipeline.joblib")
print("Model, preprocessing pipeline, and feature means saved.")
