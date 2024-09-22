import subprocess
from flask import Blueprint, jsonify
from WQMS import app



@app.route('/run-model', methods=['GET'])
def run_model():
    script_path = 'WQMS_/WQMS/water_prediction_model.py'
    
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        return jsonify({"message": "Script executed successfully", "output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Error executing script", "error": e.stderr}), 500
