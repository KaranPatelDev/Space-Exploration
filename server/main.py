from flask import Flask, request, jsonify, send_file
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to the Space Launch API!'}), 200

# Load dataset
data = pd.read_csv('dataset/launches.csv', encoding='latin1')

# Encode orbit types
le_orbit = LabelEncoder()
data['Orbit_Type_Encoded'] = le_orbit.fit_transform(data['Orbit Type'].fillna('Unknown'))

# Function to predict orbit location based on orbit type and application
def predict_location(orbit_type):
    if orbit_type == 'Earth Observation':
        return 'Low Earth Orbit'
    elif orbit_type == 'Navigation':
        return 'Geostationary Orbit'
    else:
        return 'Unknown Orbit'

# Endpoint to get all launches
@app.route('/launches', methods=['GET'])
def get_launches():
    return data.to_json(orient='records'), 200

# Endpoint to get a specific launch by ID
@app.route('/launches/<int:id>', methods=['GET'])
def get_launch(id):
    result = data[data['SL No'] == id]
    if not result.empty:
        return result.to_json(orient='records'), 200
    else:
        return jsonify({'message': 'Launch not found'}), 404

# Endpoint to predict orbit location for a single launch
@app.route('/predict', methods=['POST'])
def predict():
    data_input = request.json
    orbit_type = data_input.get('Orbit Type')
    location = predict_location(orbit_type)
    
    return jsonify({'predicted_location': location}), 200

# Endpoint to update a launch's location by ID
@app.route('/launches/<int:id>', methods=['PUT'])
def update_launch(id):
    data_input = request.json
    new_location = data_input.get('location')

    index = data[data['SL No'] == id].index
    if not index.empty:
        data.at[index[0], 'Orbit Type'] = new_location
        return jsonify({'message': 'Launch location updated successfully'}), 200
    else:
        return jsonify({'message': 'Launch not found'}), 404

# New endpoint to generate a graph of Earth-related satellites and their predicted orbit locations
@app.route('/plot-earth-orbits', methods=['GET'])
def plot_earth_orbit_predictions():
    # Filter data for satellites around Earth (e.g., Earth Observation, Navigation)
    earth_orbits = ['Low Earth Orbit', 'Geostationary Orbit', 'Medium Earth Orbit']  # Add more if needed
    earth_satellites = data[data['Orbit Type'].isin(earth_orbits)]
    
    # Create lists for satellite names and predicted orbits
    satellite_names = earth_satellites['Launch Vehicle'].tolist()
    orbit_predictions = earth_satellites['Orbit Type'].apply(predict_location).tolist()
    
    # Plot the graph using matplotlib
    plt.figure(figsize=(10, 6))
    plt.barh(satellite_names, orbit_predictions, color='green')
    plt.xlabel('Predicted Orbit')
    plt.ylabel('Satellite Name')
    plt.title('Earth Satellites and Predicted Orbit Locations')

    # Save the plot to an in-memory buffer
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    # Send the image as a response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
