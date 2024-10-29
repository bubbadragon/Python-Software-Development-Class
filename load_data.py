import streamlit as st
from data_fetcher import DataFetcher
from data_visual import DataVisualizer
from data_storage import DataStorage
from logger_setup import logger

# Load data
st.title("Weather Data Analysis")
logger.info("Starting the data processing workflow...")

# Load dataset
file = ["weather_data/Weather Training Data.csv"]
fetchers = DataFetcher.load_multiple_files(file)
data = fetchers[0].data if fetchers else None

if data is None:
    st.error("No data available to process.")
    st.stop()

# Step 1: User selects analysis mode - specific location or all locations
st.sidebar.header("Location Selection")
location_choice = st.sidebar.radio("Analyze data for:", ["All Locations", "Specific Location"])

# Initialize the DataVisualizer with the chosen dataset
if location_choice == "Specific Location":
    # Get the specific location input
    location = st.sidebar.text_input("Enter the location to analyze (e.g., Albury)")
    
    if location:
        visual = DataVisualizer(data)
        filtered_data = visual.filter_data(location=location)
        
        if filtered_data is not None:
            st.write(f"Data for location: {location}")
            st.dataframe(filtered_data)
            # Update the DataVisualizer instance to use the filtered data
            visual = DataVisualizer(filtered_data)
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

# Perform actions based on user's choice
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
