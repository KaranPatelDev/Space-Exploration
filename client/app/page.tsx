'use client';
import { useEffect, useState } from 'react';
import * as THREE from 'three';
import axios from 'axios';

// Define types for the satellite object
interface Satellite {
  LaunchVehicle: string;
  OrbitType: string;
  predicted_location: string;
}

export default function Home() {
  const [satellites, setSatellites] = useState<Satellite[]>([]);

  useEffect(() => {
    // Fetch data from Flask API when the component mounts
    const fetchSatellites = async () => {
      try {
        const res = await axios.post('http://localhost:5000/predict-orbits', {}, {
          headers: { 'Content-Type': 'application/json' }
        });

        // Use the data from the response
        const data: Satellite[] = res.data;
        setSatellites(data);
      } catch (error) {
        console.error('Error fetching satellites:', error);
      }
    };

    fetchSatellites();

    // Set up the scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Create a sphere to represent the Earth
    const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
    const earthMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const earth = new THREE.Mesh(earthGeometry, earthMaterial);
    scene.add(earth);

    // Function to create an orbit path
    function createOrbit(radius: number) {
      const curve = new THREE.EllipseCurve(
        0, 0,
        radius, radius,
        0, 2 * Math.PI,
        false,
        0
      );

      const points = curve.getPoints(50);
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
      const orbit = new THREE.Line(geometry, material);
      return orbit;
    }

    // Add satellites and their orbits when data is fetched
    satellites.forEach((sat: Satellite) => {
      let orbitRadius = 3; // Default to Low Earth Orbit radius

      if (sat.predicted_location === 'Geostationary Orbit') {
        orbitRadius = 6;
      } else if (sat.predicted_location === 'Medium Earth Orbit') {
        orbitRadius = 4.5;
      }

      const orbit = createOrbit(orbitRadius);
      scene.add(orbit);
    });

    // Set up the camera position
    camera.position.z = 10;

    // Animate the scene
    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }
    animate();
  }, [satellites]); // Dependency array ensures this effect runs when `satellites` changes

  return <div />;
}
