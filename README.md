# CSV Data Analysis and Visualization Web Application

This project is a Flask web application that allows users to upload CSV files, perform data analysis, filter data, and visualize selected columns. The application dynamically creates database tables based on uploaded files and provides a user-friendly interface for analysis.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Notes](#notes)
- [Future Improvements](#future-improvements)

---

## Features

1. **CSV File Upload**:
   - Allows users to upload CSV files.
   - Dynamically creates tables in an SQLite database based on the structure of the uploaded CSV.

2. **Data Analysis**:
   - Options to describe data for a specific column or the entire dataset.
   - Filter data based on user-defined thresholds (greater than, less than, equal to) for numeric columns.

3. **Data Visualization**:
   - Select specific columns for the X and Y axes and visualize data.
   - Filter visualizations by location, if the `location` column exists in the dataset.

4. **Dynamic Column and Location Selection**:
   - The application retrieves column names and unique locations for filtering and visualizing data, allowing flexibility with different CSV structures.

---

## Requirements

The application requires the following Python packages:

- `Flask` - For building the web application.
- `SQLAlchemy` - For interacting with the SQLite database.
- `Pandas` - For data manipulation.
- `Matplotlib` - For data visualization.

These dependencies are listed in the `requirements.txt` file.

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>

2. python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt

4. flask run

