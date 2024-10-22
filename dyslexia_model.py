import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import pickle

# Load your dataset
df = pd.read_csv('Dataset-Dyslexia-BCA(1).csv')

# Fill missing values with mode
df = df.fillna(df.mode().iloc[0])

# Encode categorical variables to numeric using LabelEncoder
label_encoders = {}
for column in df.columns:
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        label_encoders[column] = le

# Define relevant features and target
features = ['DRW', 'DIS', 'DSIS', 'DLL', 'DLSL', 'DUW', 'DRWI', 'DRA', 'DRGL', 'DMW', 'DS', 'DRC']
X = df[features]
y = df['PD']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Handle imbalance using SMOTE
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

# Train an SVM model with selected features
svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train_res, y_train_res)

# Predict using the test set
y_pred = svm_model.predict(X_test)

# Evaluate model accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy of the SVM model:", accuracy * 100)

# Show confusion matrix and classification report
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model and label encoders
with open('svm_model.pkl', 'wb') as model_file:
    pickle.dump(svm_model, model_file)

with open('label_encoders.pkl', 'wb') as le_file:
    pickle.dump(label_encoders, le_file)
