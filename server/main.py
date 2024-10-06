from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to the Space Launch API!'}), 200

data = pd.read_csv('dataset/launches.csv', encoding='latin1')

le_orbit = LabelEncoder()
data['Orbit_Type_Encoded'] = le_orbit.fit_transform(data['Orbit Type'].fillna('Unknown'))

def predict_location(launch_vehicle, orbit_type, application):
    if orbit_type == 'Earth Observation':
        return 'Low Earth Orbit'
    elif orbit_type == 'Navigation':
        return 'Geostationary Orbit'
    else:
        return 'Unknown Orbit'

@app.route('/launches', methods=['GET'])
def get_launches():
    return data.to_json(orient='records'), 200

@app.route('/launches/<int:id>', methods=['GET'])
def get_launch(id):
    result = data[data['SL No'] == id]
    if not result.empty:
        return result.to_json(orient='records'), 200
    else:
        return jsonify({'message': 'Launch not found'}), 404

@app.route('/predict', methods=['POST'])
def predict():
    data_input = request.json
    launch_vehicle = data_input.get('Launch Vehicle')
    orbit_type = data_input.get('Orbit Type')
    application = data_input.get('Application')

    location = predict_location(launch_vehicle, orbit_type, application)
    
    return jsonify({'predicted_location': location}), 200

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

@app.route('/earth-orbit-satellites', methods=['GET'])
def get_earth_orbit_satellites():
    earth_orbit_satellites = data[data['Orbit Type'].isin(['Low Earth Orbit', 'Geostationary Orbit'])]
    return earth_orbit_satellites.to_json(orient='records'), 200

@app.route('/earth-applications', methods=['GET'])
def get_earth_applications():
    earth_applications = data[data['Application'].str.contains('Earth', case=False, na=False)]
    return earth_applications.to_json(orient='records'), 200

if __name__ == '__main__':
    app.run(debug=True)
