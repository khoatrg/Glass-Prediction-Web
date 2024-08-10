import uuid
from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/analyze_glass', methods=['POST'])
def analyze_glass():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print('data as JSON:', data)

            if not data:
                raise ValueError("No data provided")

            data = list(data.values())
            print('data as list:', data)

            data = list(map(float, data))
            print('data as float:', data)

            # Ensure the data is in the correct format for the model
            expected_number_of_features = 9  # Replace with the actual number of features expected by your model
            if len(data) != expected_number_of_features:
                raise ValueError(f"Expected {expected_number_of_features} features, but got {len(data)}")

            # Add your model prediction code here
            result = model.predict([data])
            response = jsonify(result=result.tolist())
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/analyze_glass', methods=['OPTIONS'])
def analyze_glass_options():
    response = jsonify(status="OK")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
    return response

if __name__ == '__main__':
    app.run()