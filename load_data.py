import streamlit as st
import pandas as pd
from data_fetcher import DataFetcher
from data_visual import DataVisualizer
from data_storage import DataStorage
from logger_setup import logger
import joblib
import numpy as np

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Go to Prediction Page"):
    st.session_state["page"] = "prediction"
if st.sidebar.button("Back to Main Page"):
    st.session_state["page"] = "main"

# Load data
logger.info("Starting the data processing workflow...")
file = ["weather_data/Weather Training Data.csv"]
fetchers = DataFetcher.load_multiple_files(file)
data = fetchers[0].data if fetchers else None

if data is None:
    st.error("No data available to process.")
    st.stop()

# Main Page Logic
if st.session_state["page"] == "main":
    st.title("Weather Data Analysis and Prediction")

    # Step 1: User selects analysis mode - specific location or all locations
    st.sidebar.header("Location Selection")
    location_choice = st.sidebar.radio("Analyze data for:", ["All Locations", "Specific Location"])

    if location_choice == "Specific Location":
        location = st.sidebar.text_input("Enter the location to analyze (e.g., Albury)")
        if location:
            visual = DataVisualizer(data)
            filtered_data = visual.filter_data(location=location)

            if filtered_data is not None:
                st.write(f"Data for location: {location}")
                st.dataframe(filtered_data)
                visual = DataVisualizer(filtered_data)  # Update DataVisualizer instance
            else:
                st.warning("No data found for the specified location.")
                st.stop()
    else:
        st.write("Analyzing data for all locations")
        visual = DataVisualizer(data)
        st.dataframe(data)

    # Step 2: User selects action to perform on the chosen dataset
    st.sidebar.header("Data Analysis Actions")
    action = st.sidebar.selectbox("Choose an action to perform", ["Select an action", "Describe", "Head", "Plot", "Filter by Column"])

    if action == "Describe":
        if st.button("Show Description"):
            description = visual.visualize_data(action="describe")
            st.write("Data Description")
            st.write(description)
    elif action == "Head":
        num_rows = st.number_input("Number of rows to display", min_value=1, max_value=100, value=5)
        if st.button("Show Head"):
            head_data = visual.visualize_data(action="head").head(num_rows)
            st.write("First few rows of data")
            st.dataframe(head_data)
    elif action == "Plot":
        column = st.selectbox("Select column to plot", data.columns)
        log_scale = st.checkbox("Log Scale")
        if st.button("Generate Plot"):
            st.write(f"Plotting column: {column}")
            visual.plot_data(column=column, log_scale=log_scale)
    elif action == "Filter by Column":
        column = st.selectbox("Select column to filter", data.columns)
        comparison = st.selectbox("Select comparison type", ["greater", "less", "equal"])
        threshold = st.number_input(f"Enter the threshold value for {column}")
        if st.button("Filter Data"):
            filtered_data = visual.filter_data(column=column, comparison=comparison, threshold=threshold)
            if filtered_data is not None:
                st.write(f"Filtered data for {column} {comparison} {threshold}")
                st.dataframe(filtered_data)
            else:
                st.warning("No data matches the filter criteria.")

    # Step 3: Option to save the data
    st.sidebar.header("Save Data")
    save_format = st.sidebar.selectbox("Choose file format to save", ["None", "CSV", "JSON", "Excel"])
    if save_format != "None" and st.sidebar.button("Save Data"):
        storage = DataStorage(data)
        file_path = f"output.{save_format.lower()}"
        storage.save_data(file_path, file_type=save_format.lower())
        st.sidebar.success(f"Data saved successfully as {file_path}")

# Prediction Page Logic
elif st.session_state["page"] == "prediction":
    st.title("Rain Prediction")
    st.write("This page allows you to predict whether it will rain tomorrow based on weather data.")

    # Load the pre-trained model
    MODEL_PATH = "decision_tree_model_with_pipeline.joblib"
    try:
        model_data = joblib.load(MODEL_PATH)
        model = model_data["model"]
        preprocessor = model_data["preprocessor"]
        default_values = model_data["feature_means"]
        st.success("Model and preprocessing pipeline loaded successfully!")
    except FileNotFoundError:
        st.error("Model file not found.")
        st.stop()

    # Sidebar for user inputs
    user_input = {}
    required_features = list(preprocessor.feature_names_in_)
    for feature in required_features:
        user_input[feature] = st.number_input(
            label=f"{feature}",
            value=default_values.get(feature, 0.0),
        )

    # Convert user inputs to DataFrame
    input_data = pd.DataFrame([user_input])

    # Ensure input_data has all required columns
    for column in preprocessor.feature_names_in_:
        if column not in input_data.columns:
            input_data[column] = default_values.get(column, 0)

    # Preprocess user input
    input_data_processed = preprocessor.transform(input_data)

    # Predict Button
    if st.button("Predict RainTomorrow"):
        prediction = model.predict(input_data_processed)
        prediction_proba = model.predict_proba(input_data_processed)

        st.write("### Prediction Result")
        if prediction[0] == 1:
            st.success("It is likely to rain tomorrow! 🌧️")
        else:
            st.info("It is unlikely to rain tomorrow. ☀️")

        st.write("### Prediction Probability")
        st.write(f"Probability of rain: {prediction_proba[0][1]:.2f}")
        st.write(f"Probability of no rain: {prediction_proba[0][0]:.2f}")
