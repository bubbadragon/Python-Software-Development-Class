from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy import inspect
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib

# Use Agg backend for Matplotlib in non-GUI environments
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Define the path to the database file
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'uploaded_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Function to sanitize the file name for use as a SQL table name
def sanitize_table_name(file_name):
    table_name = re.sub(r'\W+', '_', os.path.splitext(file_name)[0])
    return table_name.lower()

# Route to dynamically load column names for a selected table
@app.route('/get_columns', methods=['POST'])
def get_columns():
    table_name = request.json.get('table')
    if not table_name:
        return jsonify({"error": "No table selected"}), 400

    try:
        # Load the table to retrieve its columns
        data = pd.read_sql_table(table_name, db.engine)
        columns = list(data.columns)
        return jsonify({"columns": columns})
    except Exception as e:
        print(f"Error retrieving columns for table {table_name}: {e}")
        return jsonify({"error": "Could not retrieve columns"}), 500

# Route for the main page with an upload form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                data = pd.read_csv(file)
                table_name = sanitize_table_name(file.filename)
                
                metadata = MetaData()
                inspector = inspect(db.engine)
                
                # Drop table if it already exists
                if inspector.has_table(table_name):
                    table = Table(table_name, metadata, autoload_with=db.engine)
                    table.drop(db.engine)
                
                # Dynamically create table columns based on CSV headers
                columns = [Column("id", Integer, primary_key=True)]
                for column_name in data.columns:
                    columns.append(Column(column_name, String(255)))
                
                table = Table(table_name, metadata, *columns)
                metadata.create_all(db.engine)
                data.to_sql(table_name, db.engine, if_exists='append', index=False)
                
                flash(f'Data successfully uploaded and stored in the table "{table_name}".', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
        else:
            flash('Please upload a valid CSV file.', 'error')
        
        return redirect(url_for('index'))
    
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return render_template('index.html', tables=tables)

# Route for analyzing data with options to describe, filter, or visualize
@app.route('/analyze', methods=['POST'])
def analyze_data():
    table_name = request.form.get('table')
    action = request.form.get('action')
    row_limit = request.form.get('row_limit')

    try:
        row_limit = int(row_limit) if row_limit else 20
    except ValueError:
        flash("Invalid row limit. Displaying default 20 rows.", "error")
        row_limit = 20

    if not table_name or not action:
        flash("Please select a table and an action.", "error")
        return redirect(url_for('index'))
    
    try:
        data = pd.read_sql_table(table_name, db.engine)
    except Exception as e:
        flash(f"Error loading table '{table_name}': {e}", "error")
        return redirect(url_for('index'))

    columns = list(data.columns) if data is not None else []
    analysis_result = None
    plot_url = None

    if action == "describe":
        describe_column = request.form.get('describe_column')
        if describe_column and describe_column in data.columns:
            analysis_result = data[describe_column].describe().to_frame().to_html()
            flash(f"Description of '{describe_column}' generated successfully.", "success")
        else:
            analysis_result = data.describe().to_html()
            flash("Data description generated successfully.", "success")
    
    elif action == "filter":
        column = request.form.get('column')
        comparison = request.form.get('comparison')
        threshold = request.form.get('threshold')
        if column and comparison and threshold:
            try:
                threshold = float(threshold)
                if pd.api.types.is_numeric_dtype(data[column]):
                    if comparison == "greater":
                        filtered_data = data[data[column] > threshold]
                    elif comparison == "less":
                        filtered_data = data[data[column] < threshold]
                    elif comparison == "equal":
                        filtered_data = data[data[column] == threshold]
                    analysis_result = filtered_data.head(row_limit).to_html()
                    flash("Data filtered successfully.", "success")
                else:
                    flash(f"Column '{column}' is not numeric.", "error")
            except ValueError:
                flash("Invalid threshold value.", "error")
        else:
            flash("Please provide valid filter criteria.", "error")
    
    elif action == "visualize":
        location = request.form.get('location')
        x_column = request.form.get('x_column')
        y_column = request.form.get('y_column')
        if x_column and y_column and x_column in data.columns and y_column in data.columns:
            if location and 'location' in data.columns:
                data = data[data['location'] == location]
            plt.figure(figsize=(10, 6))
            plt.plot(data[x_column].head(row_limit), data[y_column].head(row_limit), marker='o')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'{y_column} vs {x_column} for {location if location else "all locations"}')
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
            buf.close()
            plt.close()
        else:
            flash("Please select valid columns for X and Y axes.", "error")
    
    return render_template(
        'index.html', 
        tables=inspect(db.engine).get_table_names(), 
        selected_table=table_name,
        columns=columns,
        analysis_result=analysis_result,
        row_limit=row_limit,
        plot_url=plot_url
    )