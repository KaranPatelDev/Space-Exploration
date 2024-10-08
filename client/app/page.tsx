'use client';

import { useState, useEffect } from 'react';

const SpaceXPrediction = () => {
  const [launchDetails, setLaunchDetails] = useState([]);
  const [predictionResults, setPredictionResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetching launch details from the Flask API
  const fetchLaunchDetails = async () => {
    try {
      const response = await fetch('http://localhost:5000/isro-launch-details');
      const data = await response.json();
      setLaunchDetails(data);
    } catch (error) {
      console.error('Error fetching launch details:', error);
    }
  };

  useEffect(() => {
    fetchLaunchDetails();
  }, []);

  // Function to make a POST request to predict launches
  const predictLaunches = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/predict-launches', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* Payload for the prediction */ }),
      });
      const data = await response.json();
      setPredictionResults(data);
    } catch (error) {
      console.error('Error predicting launches:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>SpaceX Predictions</h1>
      <button onClick={predictLaunches} disabled={loading}>
        {loading ? 'Predicting...' : 'Predict Launches'}
      </button>
      
      {predictionResults.length > 0 && (
        <div>
          <h2>Prediction Results:</h2>
          <ul>
            {predictionResults.map((result, index) => (
              <li key={index}>
                {result['Launch Vehicle']}: {result['Predicted Application']}
              </li>
            ))}
          </ul>
        </div>
      )}

      <h2>Launch Details:</h2>
      <ul>
        {launchDetails.launch_vehicles && launchDetails.launch_vehicles.map((vehicle, index) => (
          <li key={index}>{vehicle}</li>
        ))}
      </ul>
    </div>
  );
};

export default SpaceXPrediction;
