function updateCardValues() {
  fetch('http://192.168.43.139:5000/send_data') // Fetch data from the server
    .then(response => response.json()) // Parse the JSON data
    .then(data => {
      console.log('Data received:', data); // Log data to the console for inspection
      if (data.length > 0) { // Check if data is available
        // Access the most recent entry (last element in the array)
        let latestData = data[data.length - 1];

        // Update Temperature Card
        document.getElementById('temperatureValue').textContent = latestData.temperature + '°C';

        // Update Turbidity Card
        document.getElementById('turbidityValue').textContent = latestData.turbidity + ' NTU';

        // Update TDS Card
        document.getElementById('tdsValue').textContent = latestData.tds + ' ppm';
      }
    })
    .catch(error => {
      console.error('Error fetching real-time data:', error); // Log any errors
    });
}

// Call the updateCardValues function periodically
setInterval(updateCardValues, 5000); // Every 5 seconds
