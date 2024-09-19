import os
import pandas as pd
import subprocess
from flask import Blueprint, request, jsonify, render_template, Response, send_from_directory
from WQMS import db, mail
from WQMS.models import SensorData
from werkzeug.utils import secure_filename
from flask_mail import Message
from datetime import datetime

routes = Blueprint('routes', __name__)

alert_interval = 43200  # 12 hours in seconds
last_alert_time = None

thresholdValues = {
    'temperature': 32,
    'turbidity': 900,
    'tds': 350
}

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join('WQMS/resource', filename)
        file.save(filepath)
        
        # Process the file if needed
        data = pd.read_csv(filepath)
        
        # Example: Saving data to database
        for _, row in data.iterrows():
            new_data = SensorData(sensor_value=row['value'])  # Adjust according to your CSV structure
            db.session.add(new_data)
        db.session.commit()
        
        return jsonify({'message': 'File successfully uploaded and processed'}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 400

@routes.route('/data/<filename>')
def serve_data_file(filename):
    # Use absolute path for data_folder
    data_folder = os.path.abspath('WQMS/data')
    file_path = os.path.join(data_folder, filename)
    
    # Debug: print to verify file path and existence
    print(f"Looking for file at: {file_path}")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print("File not found!")
        return jsonify({'message': f'File {filename} could not be found.'}), 404
    
    print("File found, serving it now...")
    
    try:
        # Serve the requested file
        return send_from_directory(data_folder, filename)
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({'message': f'Error serving file: {str(e)}'}), 500
    
@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/table')
def table():
    return render_template('table.html')

@routes.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        print(data)

        sensor_data = SensorData(
            temperature=data.get('temperature'),
            tds=data.get('tds'),
            turbidity=data.get('turbidity')
        )

        db.session.add(sensor_data)
        db.session.commit()

        send_email_alert(data, thresholdValues)

        return "Data received and saved successfully", 200
    except Exception as e:
        return str(e), 400

def send_email_alert(data, thresholdValues):
    global last_alert_time

    current_time = datetime.now()

    if not last_alert_time or (current_time - last_alert_time).seconds >= alert_interval:
        last_alert_time = current_time
        msg = Message('Sensor Data Alert', sender='okloelvito@gmail.com', recipients=['oklosamuel50@gmail.com'])
        alert_message = ''

        if data.get('temperature') > thresholdValues['temperature']:
            alert_message += 'Temperature value exceeded the threshold.\n'

        if data.get('turbidity') > thresholdValues['turbidity']:
            alert_message += 'Turbidity value exceeded the threshold.\n'

        if data.get('tds') > thresholdValues['tds']:
            alert_message += 'TDS value exceeded the threshold.\n'

        if alert_message:
            msg.body = alert_message
            mail.send(msg)

@routes.route('/send_data', methods=['GET'])
def get_data():
    try:
        data = SensorData.query.all()
        data_list = [{'timestamp': item.timestamp, 'temperature': item.temperature, 'tds': item.tds, 'turbidity': item.turbidity} for item in data]
        return jsonify(data_list), 200
    except Exception as e:
        return str(e), 400

@routes.route('/export_csv', methods=['GET'])
def export_csv():
    try:
        data = SensorData.query.all()
        if not data:
            return 'No data to export', 404

        df = pd.DataFrame([{'timestamp': entry.timestamp, 'temperature': entry.temperature, 'tds': entry.tds, 'turbidity': entry.turbidity} for entry in data])
        csv_data = df.to_csv(index=False)

        response = Response(csv_data, content_type='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        return response
    except Exception as e:
        return str(e), 400
    
@routes.route('/view-images')
def view_images():
    # Absolute path to the data folder where PNGs are stored
    data_folder = os.path.abspath('WQMS/data')

    # Get list of all PNG files in the data folder
    try:
        images = [f for f in os.listdir(data_folder) if f.endswith('.png')]
        if not images:
            return render_template('view_images.html', images=[])
    except Exception as e:
        return render_template('view_images.html', images=[], error=f"Error accessing data folder: {str(e)}")

    # Render the image list on a webpage
    return render_template('view_images.html', images=images)

@routes.route('/images/<filename>')
def serve_image(filename):
    data_folder = os.path.abspath('WQMS/data')
    file_path = os.path.join(data_folder, filename)

    # Debug: print to verify file path and existence
    print(f"Looking for image at: {file_path}")

    # Check if the file exists
    if not os.path.exists(file_path) or not filename.endswith('.png'):
        return jsonify({'message': f'Image {filename} could not be found.'}), 404

    print("Image found, serving it now...")
    
    try:
        # Serve the requested PNG image
        return send_from_directory(data_folder, filename)
    except Exception as e:
        print(f"Error serving image: {str(e)}")
        return jsonify({'message': f'Error serving image: {str(e)}'}), 500
