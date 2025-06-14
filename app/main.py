from flask import Flask, request, jsonify
import os
import pandas as pd
from model import train_model, predict_downtime
from utils import save_file

app = Flask(__name__)
UPLOAD_DIRECTORY = "data"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.route("/")
def hello_world():
    return jsonify(message="Welcome to the Manufacturing API!")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify(message="No file part"), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify(message="No selected file"), 400

    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        file.save(file_path)
        return jsonify(message="File uploaded successfully"), 200
    except Exception as e:
        return jsonify(message=str(e)), 400

@app.route("/train", methods=["POST"])
def train():
    try:
        dataset_path = os.path.join(UPLOAD_DIRECTORY, "sample_data.csv")
        model, accuracy, f1_score = train_model(dataset_path)
        return jsonify(accuracy=accuracy, f1_score=f1_score), 200
    except Exception as e:
        return jsonify(message=str(e)), 400

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        hydraulic_pressure = data.get("Hydraulic_Pressure(bar)")
        coolant_pressure = data.get("Coolant_Pressure(bar)")
        air_system_pressure = data.get("Air_System_Pressure(bar)")
        coolant_temperature = data.get("Coolant_Temperature")
        hydraulic_oil_temperature = data.get("Hydraulic_Oil_Temperature(?C)")
        spindle_bearing_temperature = data.get("Spindle_Bearing_Temperature(?C)")
        spindle_vibration = data.get("Spindle_Vibration(?m)")
        tool_vibration = data.get("Tool_Vibration(?m)")
        spindle_speed = data.get("Spindle_Speed(RPM)")
        voltage = data.get("Voltage(volts)")
        torque = data.get("Torque(Nm)")
        cutting = data.get("Cutting(kN)")

        if None in [hydraulic_pressure, coolant_pressure, air_system_pressure, coolant_temperature,
                    hydraulic_oil_temperature, spindle_bearing_temperature, spindle_vibration,
                    tool_vibration, spindle_speed, voltage, torque, cutting]:
            return jsonify({"message": "Missing required parameters"}), 400

        prediction_str, confidence = predict_downtime(
            hydraulic_pressure, coolant_pressure, air_system_pressure, coolant_temperature,
            hydraulic_oil_temperature, spindle_bearing_temperature, spindle_vibration,
            tool_vibration, spindle_speed, voltage, torque, cutting
        )

        return jsonify({
            "prediction": prediction_str,
            "confidence": confidence
        })
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
