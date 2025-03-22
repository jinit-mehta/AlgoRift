from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Define a route to upload and process CSV files
@app.route('/upload', methods=['POST'])
def upload_files():
    # Check if files are present in the request
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    results = []

    for file in files:
        if file.filename.endswith('.csv'):
            try:
                # Read the CSV file
                df = pd.read_csv(file)
                # Perform some operations on the DataFrame
                # Example: Calculate the mean of a column named 'value'
                mean_value = df['value'].mean()
                results.append({
                    "filename": file.filename,
                    "mean_value": mean_value
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "error": str(e)
                })
        else:
            results.append({
                "filename": file.filename,
                "error": "File is not a CSV"
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)