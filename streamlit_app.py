import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Load saved components
with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Streamlit user interface for prediction
st.title('Dyslexia Prediction Tool')

# Define the 12 relevant features for input
features = ['DRW', 'DIS', 'DSIS', 'DLL', 'DLSL', 'DUW', 'DRWI', 'DRA', 'DRGL', 'DMW', 'DS', 'DRC']

# Create input fields for each relevant feature
input_data = {}
for feature in features:
    options = sorted(list(set(label_encoders[feature].classes_)))  # List unique class options for each feature
    selected_value = st.selectbox(f'Select value for {feature}:', options=options)
    input_data[feature] = selected_value


if st.button('Predict Dyslexia'):
    try:
        # Encode the input data
        encoded_data = [label_encoders[feature].transform([input_data[feature]])[0] for feature in features]

        # Ensure the input matches the expected number of features
        assert len(encoded_data) == len(features), "The input does not match the expected number of features."

        # Wrap the encoded data to form a 2D array
        input_data_2d = [encoded_data]  # This makes it a 2D array

        # Make prediction
        prediction = model.predict(input_data_2d)
        result = 'Has Dyslexia' if prediction[0] == 1 else 'No Dyslexia'
        st.write(f'The model predicts: **{result}**')
        
    except ValueError as e:
        st.error(f"Error: {e}")
    except AssertionError as e:
        st.error(f"Error: {e}")

