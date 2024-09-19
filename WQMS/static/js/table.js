// Function to fetch and update the table with real-time data
function updateTableData() {
  fetch('https://wqms.onrender.com/send_data') // Replace with the actual endpoint for fetching data
    .then(response => response.json())
    .then(data => {
      console.log('Data received:', data);
      // Assuming data is an array of objects with keys: timestamp, temperature, ph, turbidity, tds
      if (data.length > 0) {
        // Reverse the order of data to display the most recent data at the top
        data.reverse();

        // Get a reference to the table body
        const tableBody = document.getElementById('dataBody');
        // Clear existing rows
        tableBody.innerHTML = '';

        // Iterate over the data and create rows for each entry
        data.forEach(entry => {
          const newRow = document.createElement('tr');
          newRow.innerHTML = `
            <td>${entry.timestamp}</td>
            <td>${entry.temperature}</td>
            <td>${entry.tds}</td>
            <td>${entry.turbidity}</td>
          `;
          tableBody.appendChild(newRow);
        });
      }
    })
    .catch(error => {
      console.error('Error fetching real-time data:', error);
      console.error(error.stack);
    });
}

// Call the updateTableData function periodically (e.g., every 5 seconds)
setInterval(updateTableData, 5000); // Adjust the interval as needed

