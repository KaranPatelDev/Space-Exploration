from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Load the dataset (make sure this path is correct for your environment)
data = pd.read_csv('dataset/launches.csv', encoding='latin1')

# Function to predict orbit location based on orbit type
def predict_location(orbit_type):
    if orbit_type == 'Earth Observation':
        return 'Low Earth Orbit'
    elif orbit_type == 'Navigation':
        return 'Geostationary Orbit'
    else:
        return 'Unknown Orbit'

# Endpoint to predict orbit location for a single launch
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the request
    data_input = request.json
    orbit_type = data_input.get('Orbit Type')
    launch_vehicle = data_input.get('Launch Vehicle')
    
    # Call the function to predict location
    predicted_location = predict_location(orbit_type)
    
    # Return the response as JSON
    return jsonify({
        'Launch Vehicle': launch_vehicle,
        'predicted_location': predicted_location
    }), 200

# Endpoint to plot the orbit prediction for a single satellite
@app.route('/plot-prediction', methods=['POST'])
def plot_prediction():
    # Extract data from the request
    data_input = request.json
    launch_vehicle = data_input.get('Launch Vehicle')
    orbit_type = data_input.get('Orbit Type')

    # Predict the location using the predict function
    predicted_location = predict_location(orbit_type)

    # Create a bar chart
    plt.figure(figsize=(8, 4))
    plt.barh([launch_vehicle], [predicted_location], color='blue')
    plt.xlabel('Predicted Orbit')
    plt.ylabel('Launch Vehicle')
    plt.title(f'Orbit Prediction for {launch_vehicle}')

    # Save the plot to a buffer
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    # Send the image file as a response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
