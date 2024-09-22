document.getElementById('export-csv').addEventListener('click', function () {
<<<<<<< HEAD
    fetch('http://192.168.43.139:5000/export_csv', {
=======
    fetch('https://wqms-kwv1.onrender.com/export_csv', {
>>>>>>> 5b171305871d3bb18cfadd99d06da7d5402e1c87
        method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'data.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        console.log("helloo")
    });
});
