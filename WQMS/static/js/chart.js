// Function to fetch and update real-time data
function updateRealtimeData() {
  fetch('https://wqms.onrender.com/send_data') // Replace with the actual endpoint for fetching data
    .then(response => response.json())
    .then(data => {
      // Extract hours and minutes from the timestamp and format as "hh:mm"
      const formattedTimestamps = data.map(entry => {
        const timestamp = new Date(entry.timestamp);
        const hours = timestamp.getHours().toString().padStart(2, '0'); // Ensure two digits
        const minutes = timestamp.getMinutes().toString().padStart(2, '0'); // Ensure two digits
        return `${hours}:${minutes}`;
      });

      // Trim data to the most recent 20 data points
      const newData = data.slice(-20);
      const newTimestamps = formattedTimestamps.slice(-20);

      // Update Chart 1 (Temperature)
      chart1.data.labels = newTimestamps;
      chart1.data.datasets[0].data = newData.map(entry => entry.temperature);
      chart1.data.datasets[1].data = Array(newData.length).fill(thresholdValue1); // Add threshold data
      chart1.update();

      // Update Chart 2 (Removed pH chart update code)

      // Update Chart 3 (Turbidity)
      chart3.data.labels = newTimestamps;
      chart3.data.datasets[0].data = newData.map(entry => entry.turbidity);
      chart3.data.datasets[1].data = Array(newData.length).fill(thresholdValue3); // Add threshold data
      chart3.update();

      // Update Chart 4 (TDS)
      chart4.data.labels = newTimestamps;
      chart4.data.datasets[0].data = newData.map(entry => entry.tds);
      chart4.data.datasets[1].data = Array(newData.length).fill(thresholdValue4); // Add threshold data
      chart4.update();
    })
    .catch(error => {
      console.error('Error fetching real-time data:', error);
    });
}

// Set your threshold values here
var thresholdValue1 = 35; // Threshold for Chart 1 (Temperature)
var thresholdValue3 = 900; // Threshold for Chart 3 (Turbidity)
var thresholdValue4 = 350; // Threshold for Chart 4 (TDS)

var options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
    },
  },
};

// Create three chart instances (excluding pH chart)
var ctx1 = document.getElementById('chart1').getContext('2d');
var ctx3 = document.getElementById('chart3').getContext('2d');
var ctx4 = document.getElementById('chart4').getContext('2d');

var chart1 = new Chart(ctx1, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Temperature Graph',
        data: [],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Threshold',
        data: [],
        borderColor: 'rgba(169, 160, 160, 1)',
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      },
    ],
  },
  options: options,
});

var chart3 = new Chart(ctx3, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Turbidity Graph',
        data: [],
        backgroundColor: 'rgba(255, 206, 86, 0.2)',
        borderColor: 'rgba(255, 206, 86, 1)',
        borderWidth: 1,
      },
      {
        label: 'Threshold',
        data: [],
        borderColor: 'rgba(169, 160, 160, 1)',
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      },
    ],
  },
  options: options,
});

var chart4 = new Chart(ctx4, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'TDS Graph',
        data: [],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Threshold',
        data: [],
        borderColor: 'rgba(169, 160, 160, 1)',
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
      },
    ],
  },
  options: options,
});

// Call the updateRealtimeData function periodically (e.g., every 5 seconds)
setInterval(updateRealtimeData, 5000); // Adjust the interval as needed
